from .base import *

LANGUAGE_CODE = 'es'

AWS_IS_GZIPPED = True

MIDDLEWARE += ['django.middleware.gzip.GZipMiddleware']