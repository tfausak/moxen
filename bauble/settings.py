DEBUG = True
SECRET_KEY = 'https://docs.djangoproject.com/en/dev/ref/settings/#secret-key'

ADMINS = (
    #('First Last', 'first.last@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sq3',
    }
}

INTERNAL_IPS = (
    #'127.0.0.1',
)


# Here be dragons!
ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = 'bauble.UserProfile'
COMPRESS_OUTPUT_DIR = 'cache'
LOGIN_REDIRECT_URL = '/users/settings/'
LOGIN_URL = '/users/login/'
LOGOUT_URL = '/users/logout/'
MANAGERS = ADMINS
ROOT_URLCONF = 'bauble.urls'
SITE_ID = 1
STATIC_ROOT = './static/'
STATIC_URL = '/static/'
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'bauble',
    'compressor',
    'liberator',
    'magic',
    'profiles',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'bauble.context_processors.site',
)

TEMPLATE_DIRS = (
    './templates/',
)
