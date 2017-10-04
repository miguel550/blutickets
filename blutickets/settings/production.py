from .base import *
from urllib.parse import urlparse


STATICFILES_STORAGE = 'blutickets.storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'blutickets.storages.MediaStorage'

SECRET_KEY = os.environ['SECRET_KEY']

CSRF_COOKIE_DOMAIN = os.environ.get('CSRF_COOKIE_DOMAIN', None)

LANGUAGE_CODE = 'es'

AWS_IS_GZIPPED = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
MIDDLEWARE = [
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE += ['django.middleware.gzip.GZipMiddleware']
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

GZIP_CONTENT_TYPES = (
    'text/css',
    'text/javascript',
    'application/javascript',
    'application/x-javascript',
    'image/svg+xml',
    'image/png',
    'image/jpeg',
    'image/x-png'
)

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
CELERY_BROKER_URL = os.environ['CLOUDAMQP_URL']

redis_url = urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "{0}://{1}:{2}".format(redis_url.scheme, redis_url.hostname, redis_url.port),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": redis_url.password,
        }
    }
}
