# -*- coding: utf-8 -*-
"""
Main init file for tasking app
"""
from __future__ import unicode_literals

from django_filters import FilterSet

from tasking.models import Task, TaskOccurrence

DATETIME_LOOKUPS = [
    'exact', 'gt', 'lt', 'gte', 'lte', 'year', 'year__gt', 'year__lt',
    'year__gte', 'year__lte', 'month', 'month__gt', 'month__lt',
    'month__gte', 'month__lte', 'day', 'day__gt', 'day__lt', 'day__gte',
    'day__lte']


class TaskOccurrenceFilterSet(FilterSet):
    """
    Filterset for TaskOccurrence
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskOccurrenceFilterSet
        """
        model = TaskOccurrence
        fields = {
            'task': ['exact'],
            'date': DATETIME_LOOKUPS,
            'start_time': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'end_time': ['exact', 'gt', 'lt', 'gte', 'lte']
        }


class TaskFilterSet(FilterSet):
    """
    Filterset for Task
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskFilterSet
        """
        model = Task
        fields = {
            'locations': ['exact'],
            'status': ['exact'],
            'project': ['exact'],
            'parent': ['exact'],
            'taskoccurrence__date': DATETIME_LOOKUPS,
            'taskoccurrence__start_time': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'taskoccurrence__end_time': ['exact', 'gt', 'lt', 'gte', 'lte']
        }
