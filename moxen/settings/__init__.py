from datetime import timedelta
from djcelery import setup_loader
from os import environ
from os.path import abspath, basename, dirname, join, normpath
from sys import path

# Path
_DJANGO_ROOT = dirname(dirname(abspath(__file__)))
_SITE_ROOT = dirname(_DJANGO_ROOT)
_SITE_NAME = basename(_DJANGO_ROOT)
path.append(_DJANGO_ROOT)

# Debug
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Manager
ADMINS = (
)
MANAGERS = ADMINS

# Database
DATABASES = {
    'default': {
    }
}

# General
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
TEST_RUNNER = 'app.moxen.testrunner.TestRunner'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True

# Media
MEDIA_ROOT = normpath(join(_DJANGO_ROOT, 'media'))
MEDIA_URL = '/media/'

# Static file
STATIC_ROOT = normpath(join(_DJANGO_ROOT, 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    normpath(join(_DJANGO_ROOT, 'assets')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Secret
SECRET_KEY = environ.get('SECRET_KEY',
    'https://docs.djangoproject.com/en/dev/ref/settings/#secret-key')

# Fixture
FIXTURE_DIRS = (
    normpath(join(_DJANGO_ROOT, 'fixtures')),
)

# Template
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'app.moxen.context_processors.site',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    normpath(join(_DJANGO_ROOT, 'templates')),
)

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# URL
ROOT_URLCONF = '{}.urls'.format(_SITE_NAME)

# App
INSTALLED_APPS = (
    # Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Third party
    'compressor',
    'djcelery',
    'profiles',
    'registration',
    'south',

    # Local
    'app.magic',
    'app.moxen',
)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Celery
CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)
setup_loader()

# WSGI
WSGI_APPLICATION = 'wsgi.application'

# Compressor
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
    'compressor.filters.css_default.CssAbsoluteFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

# Registration
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'
LOGOUT_URL = '/users/logout/'

# Profiles
AUTH_PROFILE_MODULE = 'moxen.UserProfile'
