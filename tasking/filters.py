"""
Module containing the Filters for tasking app
"""
from django import forms

from django_filters import rest_framework as filters

from tasking.models import Task, TaskOccurrence

DATETIME_LOOKUPS = [
    'exact', 'gt', 'lt', 'gte', 'lte', 'year', 'year__gt', 'year__lt',
    'year__gte', 'year__lte', 'month', 'month__gt', 'month__lt',
    'month__gte', 'month__lte', 'day', 'day__gt', 'day__lt', 'day__gte',
    'day__lte']
TIME_LOOKUPS = ['exact', 'gt', 'lt', 'gte', 'lte']


class TaskOccurrenceFilterSet(filters.FilterSet):
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


class TaskFilterSet(filters.FilterSet):
    """
    Filterset for Task
    """
    date = filters.LookupChoiceFilter(
        field_name='date',
        field_class=forms.DateField,
        lookup_choices=DATETIME_LOOKUPS,
        method='filter_timing')
    start_time = filters.LookupChoiceFilter(
        field_name='start_time',
        field_class=forms.TimeField,
        lookup_choices=TIME_LOOKUPS,
        method='filter_timing')
    end_time = filters.LookupChoiceFilter(
        field_name='end_time',
        field_class=forms.TimeField,
        lookup_choices=TIME_LOOKUPS,
        method='filter_timing')

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskFilterSet
        """
        model = Task
        fields = [
            'locations', 'status', 'project', 'parent', 'date', 'start_time',
            'end_time'
        ]

    # pylint: disable=unused-argument
    def filter_timing(self, queryset, name, value):
        """
        Method to filter against task timing using TaskOccurrences
        """

        # first try the exact name
        data = self.data.get(name)
        lookup = self.data.get(f'{name}_lookup')
        query_name = f'{name}__{lookup}'

        if data is None:
            # no data was found
            return queryset

        filter_args = {query_name: data}
        # get task ids
        # pylint: disable=no-member
        task_ids = TaskOccurrence.objects.filter(**filter_args).values_list(
            'task_id', flat=True).distinct()
        return queryset.filter(id__in=task_ids)
