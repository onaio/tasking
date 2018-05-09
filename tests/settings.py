# -*- coding: utf-8 -*-
"""
Settings for tests
"""
from __future__ import unicode_literals


INSTALLED_APPS = (
    # core django apps
    'django.contrib.contenttypes',
    # third party
    'rest_framework',
    # custom
    'tasking',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "secret_key_for_testing"
