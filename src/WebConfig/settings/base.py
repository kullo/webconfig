# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
"""
Django settings for WebConfig project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..'))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'static_precompiler',

    'account',
    'notifications',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'src', 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'src', 'locale'),
]

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

ROOT_URLCONF = 'WebConfig.urls'

WSGI_APPLICATION = 'WebConfig.wsgi.application'


# try to read Docker-related env vars
KULLO_DB_ADDR = os.getenv("DB_PORT_5432_TCP_ADDR", "127.0.0.1")
KULLO_DB_PORT = os.getenv("DB_PORT_5432_TCP_PORT", "5432")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webconfig',
        'USER': 'webconfig',
        'PASSWORD': 'webconfig',
        'HOST': KULLO_DB_ADDR,
        'PORT': KULLO_DB_PORT,
        'ATOMIC_REQUESTS': True,
    },
    'kulloserver': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kullo',
        'USER': 'webconfig',
        'PASSWORD': 'webconfig',
        'HOST': KULLO_DB_ADDR,
        'PORT': KULLO_DB_PORT,
    }
}
DATABASE_ROUTERS = ['WebConfig.db_router.KulloDbRouter']

AUTHENTICATION_BACKENDS = [
    'account.auth.KulloAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en-us'

USE_TZ = True
TIME_ZONE = 'Europe/Berlin'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "static_precompiler.finders.StaticPrecompilerFinder",
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'src', 'static'),
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FROM_EMAIL = 'Kullo Support <hi@kullo.net>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
AUDIT_EMAIL = 'audit-archive@kullo.net'
