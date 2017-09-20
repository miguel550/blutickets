from .base import *

LANGUAGE_CODE = 'es'

AWS_IS_GZIPPED = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
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
