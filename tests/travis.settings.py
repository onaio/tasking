# -*- coding: utf-8 -*-
"""
Settings for tests
"""
from __future__ import unicode_literals

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ona_tasking',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1'
    }
}
