"""Django settings.
"""
ADMINS = (
    # ('First Last', 'first.last@example.com'),
)
DEBUG = True
INTERNAL_IPS = (
    # '127.0.0.1',
)
SECRET_KEY = ''

# You probably don't need to edit below this line.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sq3',
    }
}
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'liberator',
    'magic',
    'django.contrib.admindocs', # Must be last.
)
MANAGERS = ADMINS
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'bauble.urls'
SITE_ID = 1
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)
TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    './templates/',
)
