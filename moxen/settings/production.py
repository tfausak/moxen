# pylint: disable=W0401,W0614
from . import *
from . import _SITE_NAME
from memcacheify import memcacheify
from os import environ
from postgresify import postgresify

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_HOST_USER = environ.get('SENDGRID_USERNAME', '')
EMAIL_HOST_PASSWORD = environ.get('SENDGRID_PASSWORD', '')
EMAIL_SUBJECT_PREFIX = '[{}] '.format(_SITE_NAME)
SERVER_EMAIL = EMAIL_HOST_USER

# Manager
ADMINS = (
    ('Taylor Fausak', 'taylor@fausak.me'),
)
MANAGERS = ADMINS

# Database
DATABASES = postgresify()

# Cache
CACHES = memcacheify()

# Celery
BROKER_TRANSPORT = 'amqplib'
BROKER_POOL_LIMIT = 3
BROKER_CONNECTION_MAX_RETRIES = 0
BROKER_URL = environ.get('RABBITMQ_URL') or environ.get('CLOUDAMQP_URL')
CELERY_RESULT_BACKEND = 'amqp'

# Storage
INSTALLED_APPS += (
    'storages',
)
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = \
    'storages.backends.s3boto.S3BotoStorage'
AWS_CALLING_FORMAT = 2  # S3.CallingFormat.SUBDOMAIN
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age={0}, s-maxage={0}, must-revalidate'.format(
        AWS_EXPIREY)
}
STATIC_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)

# Compressor
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_CSS_FILTERS += [
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS += [
    'compressor.filters.jsmin.JSMinFilter',
]
