import os

from django.conf import settings


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():

    # a setting to determine whether we are running on OpenShift
    ON_OPENSHIFT = False
    if os.environ.has_key('OPENSHIFT_REPO_DIR'):
        ON_OPENSHIFT = True
    if os.environ.has_key('OPENSHIFT_DB_NAME'):
        DB_NAME = os.environ['OPENSHIFT_DB_NAME']
    if os.environ.has_key('OPENSHIFT_DB_USERNAME'):
        DB_USER = os.environ['OPENSHIFT_DB_USERNAME']
    if os.environ.has_key('OPENSHIFT_DB_PASSWORD'):
        DB_PASSWD = os.environ['OPENSHIFT_DB_PASSWORD']
    if os.environ.has_key('OPENSHIFT_DB_HOST'):
        DB_HOST = os.environ['OPENSHIFT_DB_HOST']
    if os.environ.has_key('OPENSHIFT_DB_PORT'):
        DB_PORT = os.environ['OPENSHIFT_DB_PORT']


    if ON_OPENSHIFT:
        # os.environ['OPENSHIFT_DB_*'] variables can be used with databases created
        # with rhc app cartridge add (see /README in this git repo)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': DB_NAME,               # Or path to database file if using sqlite3.
                'USER': DB_USER,               # Not used with sqlite3.
                'PASSWORD': DB_PASSWD,         # Not used with sqlite3.
                'HOST': DB_HOST,               # Set to empty string for localhost. Not used with sqlite3.
                'PORT': DB_PORT,               # Set to empty string for default. Not used with sqlite3.
            }
        }
    else:
    # FOR LOCAL SERVER USE
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'test_db',
                'USER': 'test',
                'PASSWORD': 'SIA_passw0rd',
                'HOST': '',
                'PORT': '',
            }
        }