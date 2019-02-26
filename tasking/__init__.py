# -*- coding: utf-8 -*-
"""
Main init file for tasking app
"""
from __future__ import unicode_literals

VERSION = (0, 2, 2)
__version__ = '.'.join(str(v) for v in VERSION)
# pylint: disable=invalid-name
default_app_config = 'tasking.apps.TaskingConfig'  # noqa
