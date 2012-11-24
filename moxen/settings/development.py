# pylint: disable=W0401,W0614
from . import *
from . import _DJANGO_ROOT
from os.path import join, normpath

# Debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(_DJANGO_ROOT, 'default.db')),
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery
CELERY_ALWAYS_EAGER = True

# Toolbar
INSTALLED_APPS += (
    'debug_toolbar',
)
INTERNAL_IPS = (
    '127.0.0.1',
)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
