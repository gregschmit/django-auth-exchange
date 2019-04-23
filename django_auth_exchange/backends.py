from django.contrib.auth import get_user_model
import exchangelib as el
from .settings import get_setting
try:
    from django_auth_exchange_organizations.models import DomainOrganization
except (ModuleNotFoundError, NameError):
    DomainOrganization = False


user_model = get_user_model()
username_field = user_model.USERNAME_FIELD or 'username'


class ExchangeAuthBackend:
    """
    This authentication backend uses ``exchangelib`` to authenticate against the
    Exchange or Office365 server.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = get_setting('AUTH_EXCHANGE_CREATE_UNKNOWN_USER')

    def authenticate(self, request, username, password):
        """
        Check for the format of the username (``dom\\user`` vs ``user@dom``),
        then authenticate, and if successful, get or create the user object and
        return it.
        """
        username = username.lower()
        allowed_formats = get_setting('AUTH_EXCHANGE_ALLOWED_FORMATS')
        if '\\' in username:
            # assume dom\user
            if 'netbios' not in allowed_formats: return None
            netbios, user = username.rsplit('\\', 1)
            try:
                dom = get_setting('AUTH_EXCHANGE_NETBIOS_TO_DOMAIN_MAP')[netbios]
            except KeyError:
                dom = netbios
            smtp = '{0}@{1}'.format(user, dom)
            c_username = username
        elif '@' in username:
            # assume user@dom
            if 'email' not in allowed_formats: return None
            user, dom = username.rsplit('@', 1)
            smtp = username
            c_username = username
        else:
            # assume username only
            if 'username' not in allowed_formats: return None
            dom = get_setting('AUTH_EXCHANGE_DEFAULT_DOMAIN')
            user = username
            smtp = "{0}@{1}".format(user, dom)
            if not '.' in dom:
                c_username = "{0}\\{1}".format(dom, user)
            else:
                c_username = "{0}@{1}".format(user, dom)

        # check if domain is allowed
        domains = get_setting('AUTH_EXCHANGE_DOMAIN_SERVERS')
        if dom not in domains: return None

        # authenticate against Exchange server
        domain_server = domains.get(dom, 'autodiscover') or 'autodiscover'
        cred = el.Credentials(username=c_username, password=password)
        if domain_server == 'autodiscover':
            acc_opts = {
                'primary_smtp_address': smtp,
                'credentials': cred,
                'autodiscover': True,
                'access_type': el.DELEGATE
            }
            try:
                acc = el.Account(**acc_opts)
            except (el.errors.UnauthorizedError, el.errors.AutoDiscoverFailed):
                return None
        else:
            cfg_opts = {
                'credentials': cred,
                'server': domain_server,
            }
            try:
                cfg = el.Configuration(**cfg_opts)
            except (el.errors.UnauthorizedError, el.errors.AutoDiscoverFailed):
                return None
            acc_opts = {
                'config': cfg,
                'primary_smtp_address': smtp,
                'credentials': cred,
                'autodiscover': False,
                'access_type': el.DELEGATE
            }
            try:
                acc = el.Account(**acc_opts)
            except (el.errors.UnauthorizedError, el.errors.AutoDiscoverFailed):
                return None
        if not acc: return None

        # auth successful, get or create local user
        try:
            u = user_model.objects.get(**{username_field: c_username})
        except user_model.DoesNotExist:
            if self.create_unknown_user:
                u = user_model.objects.create(**{username_field: c_username})
                if DomainOrganization:
                    DomainOrganization.associate_new_user(u, dom)
            else:
                return None

        # enforce domain user properties, if they exist, and save
        user_properties = get_setting('AUTH_EXCHANGE_DOMAIN_USER_PROPERTIES').get(dom, {})
        if user_properties:
            for k,v in user_properties.items():
                setattr(u, k, v)
        if '.' in dom: setattr(u, u.get_email_field_name(), c_username)
        u.save()

        return u

    def get_user(self, user_id):
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
