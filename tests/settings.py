# -*- coding: utf-8 -*-
"""
Settings for tests
"""
from __future__ import unicode_literals


INSTALLED_APPS = (
    # core django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    # third party
    'rest_framework',
    'django_filters',
    'rest_framework_gis',  # Required for CountryField in Location Model
    'django_countries',  # Required for CountryField in Location Model
    'mptt',
    # custom
    'tasking',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ona_tasking',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1'
    }
}

TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS':
        ('django_filters.rest_framework.DjangoFilterBackend',)
}

SECRET_KEY = "secret_key_for_testing"

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]


# try and load local_settings if present
try:
    # pylint: disable=wildcard-import
    # pylint: disable=unused-wildcard-import
    from .local_settings import *  # noqa
except ImportError:
    pass
