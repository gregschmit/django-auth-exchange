Auth Exchange
#############

.. inclusion-marker-do-not-remove

.. image:: https://readthedocs.org/projects/django-auth-exchange/badge/?version=latest
    :target: https://django-auth-exchange.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Documentation: https://django-auth-exchange.readthedocs.io

Source: https://github.com/gregschmit/django-auth-exchange

PyPI: https://pypi.org/project/django-auth-exchange/

Auth Exchange is a reusable Django app that allows you to authenticate users
against an Exchange/Office365 server (using ``exchangelib``).

**The Problem**: I don't want users of my app to remember another password.

**The Solution**: This app allows those users to authenticate using their
Exchange email credentials.


How to Use
==========

.. code-block:: shell

    $ pip install django-auth-exchange

Include ``django_auth_exchange`` in your ``INSTALLED_APPS``.

Add ``django_auth_exchange.backends.ExchangeAuthBackend`` to your
``AUTHENTICATION_BACKENDS``, e.g.:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        'django_auth_exchange.backends.ExchangeAuthBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

Configure at least one domain:

.. code-block:: python

    AUTH_EXCHANGE_DOMAIN_SERVERS = {
        'example.org': 'autodiscover',
    }


Settings
--------

``AUTH_EXCHANGE_CREATE_UNKNOWN_USER`` (default: ``True``) - Determines if users
should be created if they are not found in the local database.

``AUTH_EXCHANGE_DEFAULT_DOMAIN`` (default: ``'example.com'``) - If only a
username is provided, this is the default domain that will be associated.

``AUTH_EXCHANGE_ALLOWED_FORMATS`` (default:
``['email', 'netbios', 'username']``) - This specifies which formats are allowed
as the username (email means ``someuser@example.com``, netbios means
``EXAMPLE\someuser``, and username means ``someuser``).

``AUTH_EXCHANGE_DOMAIN_SERVERS`` (default: ``{}``) - This specifies the domains
which are allowed to authenticate and the server that should be used for
authentication (or ``'autodiscover'``). Hint: Office365 uses the server
``outlook.office365.com``.

``AUTH_EXCHANGE_DOMAIN_USER_PROPERTIES`` (default: ``{}``) - This specifies the
settings we should apply to a user when they are added to the local database for
each domain (e.g., to make all ``example.com`` users superusers, do:
``{'example.com': {'is_staff': True, 'is_superuser': True}}``).

``AUTH_EXCHANGE_NETBIOS_TO_DOMAIN_MAP`` (default: ``{}``) - This specifies a
mapping from NETBIOS names to domain names.


Contributing
============

Email gschmi4@uic.edu if you want to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must
make any contributions to this project available under the MIT license.

To collaborators: don't push using the ``--force`` option.
