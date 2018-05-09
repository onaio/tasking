# -*- coding: utf-8 -*-
"""
Settings for tests
"""
from __future__ import unicode_literals


INSTALLED_APPS = (
    # core django apps
    'django.contrib.contenttypes',
    'django.contrib.gis',
    # third party
    'rest_framework',
    # custom
    'tasking',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "secret_key_for_testing"
SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
