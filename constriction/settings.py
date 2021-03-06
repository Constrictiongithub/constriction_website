import logging
import os
import sys

from django.utils.translation import gettext_lazy as _
from google.oauth2 import service_account

from . import basesettings as BASESETTINGS

"""
Django settings for constriction project.

Generated by 'django-admin startproject' using Django 2.2b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJ_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = BASESETTINGS.DJANGO_SECRET_KEY
ALLOWED_HOSTS = [BASESETTINGS.HOST_NAME, ]
SECURE_SSL_REDIRECT = not BASESETTINGS.DEVELOPMENT
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = BASESETTINGS.DEVELOPMENT
TEMPLATE_DEBUG = BASESETTINGS.DEVELOPMENT

# Python dotted path to the WSGI application used by Django's runserver.
# WSGI_APPLICATION = BASESETTINGS.WSGI_APPLICATION

# Application definition
INSTALLED_APPS = [
    'contacts',
    'economics_data',
    'layout',
    'importer',
    'investments',
    'autoslug',
    'modeltranslation',
    'imagekit',
    'django_countries',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader.apps.WebpackLoaderConfig',
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    
    def show_toolbar(request):
        return False
        if request.is_ajax():
            return False
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

ROOT_URLCONF = BASESETTINGS.DJANGO_ROOT_URL

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': BASESETTINGS.DB_NAME,
        'USER': BASESETTINGS.DB_USER,
        'PASSWORD': BASESETTINGS.DB_PASSWORD,
        'HOST': 'db',
        'PORT': '5432',
    }
}

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(PROJ_DIR, 'gs_credentials.json')
)

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

COUNTRIES_ONLY = [('EU', _('Unione Europea')),
                  "IT", "CH", "GB", "FR", "DE", "IE", "LV", "EE"]

LANGUAGES = [
    ('it', _('Italiano')),
    ('en', _('Inglese')),
   # ('fr', _('Francese')),
   # ('de', _('Tedesco')),
]
MODELTRANSLATION_CUSTOM_FIELDS = ('JSONField',)
MODELTRANSLATION_AUTO_POPULATE = 'required'

LANGUAGE_CODE = 'it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'

#WEBPACK
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'layout', 'webpack-stats.json'),
        'TIMEOUT': 10
    }
}

# CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'importer': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# MANAGERS
MANAGERS = []
