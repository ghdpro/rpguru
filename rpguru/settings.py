"""RPGuru Settings file"""

import os
import configparser
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_DIR = os.environ.get('HOME')

# Load apps from 'rpguru' folder as if they were in project root
import sys
sys.path.insert(0, os.path.join(BASE_DIR, 'rpguru'))

# Load configuration from INI-like .env file
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, '.env'))

DEBUG = config.getboolean('DEFAULT', 'debug', fallback=False)
SECRET_KEY = config['DEFAULT']['secret_key']
if 'allowed_hosts' in config['DEFAULT']:
    ALLOWED_HOSTS = json.loads(config.get('DEFAULT', 'allowed_hosts'))
else:
    ALLOWED_HOSTS = ['.rpguru.com']
SITE_ID = 1
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

if 'email' in config:
    if 'default_from_email' in config['email']:
        DEFAULT_FROM_EMAIL = config.get('email', 'default_from_email')
    if 'server_email' in config['email']:
        SERVER_EMAIL = config.get('email', 'server_email')

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(FILE_DIR, 'static')

MEDIA_URL = '/artwork/'
MEDIA_ROOT = os.path.join(FILE_DIR, 'artwork')

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o775
FILE_UPLOAD_PERMISSIONS = 0o664

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-allauth
    'allauth',
    'allauth.account',
    'markdownify',
    'changerequest',
    'artwork',
    'core',
    'library'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'changerequest.middleware.ChangeRequestMiddleware'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ROOT_URLCONF = 'rpguru.urls'
WSGI_APPLICATION = 'rpguru.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '',  # unix socket
        'NAME': 'rpguru',
        'USER': 'rpguru',
        'PASSWORD': config['database']['password'],
        'TEST': {
            'NAME': 'rpguru_test'
        }
    }
}

if 'cache' in config and 'redis' in config['cache']:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config['cache']['redis'],
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient'
            },
            'KEY_PREFIX': 'rpguru'
        }
    }
elif DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

if 'email' in config:
    if 'host' in config['email']:
        EMAIL_HOST = config.get('email', 'host')
    if 'host_user' in config['email']:
        EMAIL_HOST_USER = config.get('email', 'host_user')
    if 'host_user' in config['email']:
        EMAIL_HOST_PASSWORD = config.get('email', 'host_password')
    if 'port' in config['email']:
        EMAIL_PORT = config.get('email', 'port')

AUTH_USER_MODEL = 'core.RPGuruUser'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/account/profile'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
if 'auth' in config and 'account_email_verification' in config['auth']:
    ACCOUNT_EMAIL_VERIFICATION = config.get('auth', 'account_email_verification')
else:
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_REQUIRED = True

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

# Prefer Argon2 for passwords
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Log file must be writable by Django server process
from django.utils.log import DEFAULT_LOGGING
if 'logfile' in config['DEFAULT']:
    LOGFILE = config.get('DEFAULT', 'logfile')
else:
    LOGFILE = os.path.join(FILE_DIR, 'log', 'rpguru.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(message)s [%(name)s.%(funcName)s:%(lineno)d]',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'production': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOGFILE,
            'formatter': 'verbose',
            'filters': ['require_debug_false'],
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOGFILE,
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        '': {
            'handlers': ['console', 'production', 'debug'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'production', 'debug'],
            'level': 'INFO',
            'propagate': False,
        },
        'asyncio': {
            'handlers': ['console', 'production', 'debug'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    }
}

# Sentry
if 'sentry' in config and config.getboolean('sentry', 'enable', fallback=True):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=config['sentry']['dsn'],
        integrations=[DjangoIntegration()],
        send_default_pii=True
    )

# Django Debug Toolbar
if 'debug-toolbar' in config and config.getboolean('debug-toolbar', 'enable', fallback=False):
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    INTERNAL_IPS = ('127.0.0.1',)

# Date format
from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = 'Y-m-d H:i:s'
en_formats.SHORT_DATETIME_FORMAT = 'Y-m-d H:i'
en_formats.SHORT_DATE_FORMAT = 'Y-m-d'

# Compatibility fix for the 'messages' framework and Bootstrap (error -> danger)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
