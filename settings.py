ADMINS = (
    # ('First Last', 'first.last@example.com'),
)
DEBUG = True
INTERNAL_IPS = (
    # '192.168.1.1',
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
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'liberator',
    'magic',
)
MANAGERS = ADMINS
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'bauble.urls'
SITE_ID = 1
TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    './templates/',
)
