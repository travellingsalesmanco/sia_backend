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

    if ON_OPENSHIFT:
        print("USING OPENSHIFT DB")
        # os.environ['OPENSHIFT_DB_*'] variables can be used with databases created
        # with rhc app cartridge add (see /README in this git repo)
        print(os.environ['OPENSHIFT_MYSQL_DB_HOST'])
        print(os.environ['OPENSHIFT_MYSQL_DB_PORT'])
        print(os.environ['OPENSHIFT_MYSQL_DB_NAME'])
        print(os.environ['OPENSHIFT_MYSQL_DB_USER'])
        print(os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'])

        return {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['OPENSHIFT_MYSQL_DB_NAME'],
        'USER': os.environ['OPENSHIFT_MYSQL_DB_USER'],
        'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
        'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
        'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
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