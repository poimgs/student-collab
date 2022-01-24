from .common import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# TODO: When implementing terraform, change the address dynamically
ALLOWED_HOSTS = ['server-h3j5wl475a-as.a.run.app', 'client-h3j5wl475a-as.a.run.app', 'student-collab.com', 'admin.student-collab.com']

CORS_ALLOWED_ORIGINS = ['https://student-collab.com', 'https://www.student-collab.com', 'https://admin.student-collab.com', 'https://server-h3j5wl475a-as.a.run.app', 'https://client-h3j5wl475a-as.a.run.app']

CSRF_TRUSTED_ORIGINS = ['https://student-collab.com', 'https://www.student-collab.com', 'https://admin.student-collab.com', 'https://server-h3j5wl475a-as.a.run.app', 'https://client-h3j5wl475a-as.a.run.app']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_NAME'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT']
    },
    'channels_postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_NAME'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT']
    }
}

CHANNEL_LAYERS = {
    # 'default': {
    #     'BACKEND': 'channels_redis.core.RedisChannelLayer',
    #     'CONFIG': {
    #         "hosts": [(os.environ['REDIS_HOST'], os.environ['REDIS_PORT'])],
    #     },
    'default': {
        'BACKEND': 'channels_postgres.core.PostgresChannelLayer',
        'CONFIG': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['POSTGRES_NAME'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': os.environ['POSTGRES_HOST'],
            'PORT': os.environ['POSTGRES_PORT']
        }
    },
}
