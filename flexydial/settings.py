"""
Django settings for flexydial project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import socket
import pickle, redis, re
import uuid

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#globel variable for reusefull purpose.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*^gyxflla@kwhnj6$o)n=ihi2-ntcy-)t7phnc^%p!9_a&al&!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=False))
LOGIN_URL = '/'
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'crm',
    'callcenter',
    'dialer',
    'scripts',
    'django_apscheduler',
    'django.contrib.humanize',
    'django.contrib.postgres',
    # 'debug_toolbar',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'flexydial.session_middleware.SessionIdleMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'flexydial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flexydial.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('FLEXYDIAL_DB_NAME'),
        'USER': os.environ.get('FLEXYDIAL_DB_USER'),
        'PASSWORD': os.environ.get('FLEXYDIAL_DB_PASS'),
        'HOST': os.environ.get('FLEXYDIAL_DB_HOST'),
        'PORT': os.environ.get('FLEXYDIAL_DB_PORT'),
    },
    'crm': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('CRM_DB_NAME'),
        'USER': os.environ.get('CRM_DB_USER'),
        'PASSWORD': os.environ.get('CRM_DB_PASS'),
        'HOST': os.environ.get('CRM_DB_HOST'),
        'PORT': os.environ.get('CRM_DB_PORT'),
    },
}
DATABASE_ROUTERS = ['crm.router.DbRouter','callcenter.router.DbRouter']

PSQL_DB = DATABASES['default']

# Using connection string for Autodial SQLAlchemyJobStore
DB_CSTRING = {
    'default': 'postgres://%s:%s@%s/%s' % (
        PSQL_DB['USER'], PSQL_DB['PASSWORD'], PSQL_DB['HOST'], PSQL_DB['NAME'])
    }


# Redis settings starts
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/1" % ( os.environ.get('REDIS_HOST'),os.environ.get('REDIS_PORT')),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

CACHE_TTL = 60 * 15
#Redis settings ends

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

#rest_framework permissions
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'scripts.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'scripts.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'scripts.pagination.DatatablesPageNumberPagination',
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

NODEJS_SOCKET_PORT = 3232
WEB_LIVE_STATUS_CHANNEL = 'flexydial-dashboard'

AUTH_USER_MODEL         = 'callcenter.User'
MEDIA_ROOT              = os.path.join('/var/lib/flexydial/', 'media')
MEDIA_URL               = '/media/'
RECORDING_ROOT          = '/var/spool/freeswitch/default'
RECORDING_URL           = '/recordings/'
RPC_HOST                = 'localhost'
RPC_USERNAME            = 'freeswitch'
RPC_PASSWORD            = 'works'
RPC_PORT                = '8080'
R_SERVER                = redis.Redis(connection_pool=redis.ConnectionPool(
                            host=os.environ.get('REDIS_HOST'),port=os.environ.get('REDIS_PORT'),db=0))
NDNC_URL                = 'http://127.0.0.1:5000/search/%s'
FS_ORIGINATE            = \
        "expand originate "\
        "{ignore_early_media=true,campaign='$campaign_slug',"\
        "phonebook='$phonebook_id',contact_id='$contact_id',$variables}$dial_string $campaign_extension"
# FS_MANUAL_ORIGINATE     = \
#         "{$variables,contact_id='$contact_id',ignore_early_media=false,return_ring_ready=true}$dial_string $transfer_extension"

FS_WFH_PROGRESSIVE_ORIGINATE     = \
        "{$variables,contact_id='$contact_id',ignore_early_media=false,return_ring_ready=true}$dial_string $transfer_extension"

FS_MANUAL_ORIGINATE     = "originate {$variables,contact_id='$contact_id',ignore_early_media=false,return_ring_ready=true}$dial_string $transfer_extension"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

###### To reload all static data to client ######
URL_PARAMETER = str(uuid.uuid4())

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = '/etc/apache2/sites-available/flexydial.com/'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADDRESS = s.getsockname()[0]
s.close()
INTERNAL_IPS = [IP_ADDRESS, "127.0.0.1"]

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_IDLE_TIMEOUT = 60*100
SESSION_COOKIE_AGE = 60
# resetting the password url valid days
PASSWORD_RESET_TIMEOUT_DAYS = 1

WEB_SOCKET_HOST = os.environ.get('WEB_SOCKET_HOST',"")
FREESWITCH_IP_ADDRESS = os.environ.get('FREESWITCH_HOST')
SOURCE = 'FLEXY'
LOCATION = 'Mumbai'

SSL_CERTIFICATE = "/etc/ssl/ca-flexydial.crt"
# def show_toolbar(request):
#     return True
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
# }
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

SERVICES_LIST= []