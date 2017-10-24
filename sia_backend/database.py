import os

from django.conf import settings


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():
    import os
    DJ_PROJECT_DIR = os.path.dirname(__file__)
    BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
    WSGI_DIR = os.path.dirname(BASE_DIR)
    REPO_DIR = os.path.dirname(WSGI_DIR)
    DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

    # a setting to determine whether we are running on OpenShift
    ON_OPENSHIFT = False
    if os.environ.has_key('OPENSHIFT_REPO_DIR'):
        ON_OPENSHIFT = True

    if ON_OPENSHIFT:
        print("USING OPENSHIFT DB")
        # os.environ['OPENSHIFT_DB_*'] variables can be used with databases created
        # with rhc app cartridge add (see /README in this git repo)
        return {
                'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': os.path.join(DATA_DIR, 'appdb')
        }
    else:
        print("USING LOCAL DB")
    # FOR LOCAL SERVER USE
        return {
                'ENGINE': 'django.db.backends.mysql',
                'NAME   ': 'test_db',
                'USER': 'test',
                'PASSWORD': 'SIA_passw0rd',
                'HOST': '',
                'PORT': '',
            }