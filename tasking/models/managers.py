# -*- coding: utf-8 -*-
"""
Manager module for Tasking
"""
from __future__ import unicode_literals

from django.db import models


# pylint: disable=too-few-public-methods
class TaskManager(models.Manager):
    """
    Custom manager for Task
    """

    def get_queryset(self):
        """
        Custom get_query set for Task Model
        """
        queryset = super(TaskManager, self).get_queryset()
        queryset = queryset.annotate(
            submission_count=models.Count('submission__id'))
        return queryset
