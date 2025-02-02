"""
Django settings for blutickets project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from .local import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATICFILES_STORAGE = 'blutickets.storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'blutickets.storages.MediaStorage'

SHELL_PLUS = "ipython"

INSTALLED_APPS += []

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


TIME_ZONE = 'UTC'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_STATIC_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_MEDIA_LOCATION = 'media'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../assets"),
]

MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, '../profiles/locale'),
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = "noreplyblutickets@gmail.com"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERY_BROKER_URL = "amqp://guest@192.168.99.100"
