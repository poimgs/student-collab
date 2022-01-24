from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-86wi-7bzntup+@3mb^)g$f4912_@g-h@qyv_@-h3j#v!i%%q^+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

CORS_ALLOWED_ORIGINS = ['http://localhost:3000']

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'discussion',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'postgres',
        'PORT': '5432'
    },
    'channels_postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'discussion',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'postgres',
        'PORT': '5432'
    }
}

CHANNEL_LAYERS = {
    # 'default': {
    #     'BACKEND': 'channels_redis.core.RedisChannelLayer',
    #     'CONFIG': {
    #         "hosts": [('redis', 6379)],
    #     },
    'default': {
        'BACKEND': 'channels_postgres.core.PostgresChannelLayer',
        'CONFIG': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'discussion',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'postgres',
            'PORT': '5432',
        }
    },
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
