from .base import *

LANGUAGE_CODE = 'es'

AWS_IS_GZIPPED = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
MIDDLEWARE += ['django.middleware.gzip.GZipMiddleware']

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
