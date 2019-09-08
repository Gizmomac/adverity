from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'adverity',
        'PASSWORD': 'adverity',
        'USER': 'adverity',
        'HOST': 'postgres',
    }
}
DEBUG = False

ALLOWED_HOSTS = ['*']
