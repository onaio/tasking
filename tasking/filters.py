"""
Module containing the Filters for tasking app
"""
from django_filters import rest_framework as rest_filters
from rest_framework import filters

from tasking.models import Task, TaskOccurrence

DATETIME_LOOKUPS = [
    'exact', 'gt', 'lt', 'gte', 'lte', 'year', 'year__gt', 'year__lt',
    'year__gte', 'year__lte', 'month', 'month__gt', 'month__lt',
    'month__gte', 'month__lte', 'day', 'day__gt', 'day__lt', 'day__gte',
    'day__lte']
TIME_LOOKUPS = ['exact', 'gt', 'lt', 'gte', 'lte']


class TaskOccurrenceFilterSet(rest_filters.FilterSet):
    """
    Filterset for TaskOccurrence
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskOccurrenceFilterSet
        """
        model = TaskOccurrence
        fields = {
            'task': ['exact'],
            'location': ['exact'],
            'date': DATETIME_LOOKUPS,
            'start_time': TIME_LOOKUPS,
            'end_time': TIME_LOOKUPS
        }


class TaskOccurenceFilter(filters.BaseFilterBackend):
    """
    Task filter backend that filters the TaskOccurences
    """
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        query_param_keys = query_params.keys()
        filter_args = {}

        for key in query_param_keys:
            try:
                name, lookup = key.split('__')
            except ValueError:
                pass
            else:
                if lookup in DATETIME_LOOKUPS and name == 'date':
                    filter_args[key] = query_params.get(key)

                if lookup in TIME_LOOKUPS and name in [
                        'start_time', 'end_time']:
                    filter_args[key] = query_params.get(key)

        # pylint: disable=no-member
        if filter_args:
            task_ids = TaskOccurrence.objects.filter(
                **filter_args).values_list('task_id', flat=True).distinct()
            return queryset.filter(id__in=task_ids)

        return queryset


class TaskFilterSet(rest_filters.FilterSet):
    """
    Filterset for Task
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskFilterSet
        """
        model = Task
        fields = [
            'locations', 'status', 'project', 'parent'
        ]
