# -*- coding: utf-8 -*-
"""
Apps module for tasking app
"""
from __future__ import unicode_literals

from django.apps import AppConfig


class TaskingConfig(AppConfig):
    """
    Tasking App Config Class
    """
    name = 'tasking'

    def ready(self):
        # pylint: disable=unused-variable
        import tasking.signals  # noqa
