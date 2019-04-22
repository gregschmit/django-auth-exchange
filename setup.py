import os
from setuptools import find_packages, setup
from django_auth_exchange import version


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# stamp the package prior to installation
version.stamp_directory(os.path.join(os.getcwd(), 'django_auth_exchange'))

# get README
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='django-auth-exchange',
    version=version.get_version(),
    packages=find_packages(),
    include_package_data=True,
    package_data={'django_auth_exchange': ['VERSION_STAMP']},
    description='A reusable Django app for authenticating against Exchange servers.',
    long_description="long_description",
    install_requires=['Django>=2', 'exchangelib'],
    url='https://github.com/gregschmit/django-auth-exchange',
    author='Gregory N. Schmit',
    author_email='gschmi4@uic.edu',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
