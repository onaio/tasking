"""
TaskOccurrence viewsets
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from tasking.models import TaskOccurrence
from tasking.serializers import TaskOccurrenceSerializer
from tasking.filters import TaskOccurrenceFilterSet


# pylint: disable=too-many-ancestors
class TaskOccurrenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for occurrence
    """
    serializer_class = TaskOccurrenceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filter_class = TaskOccurrenceFilterSet
    ordering_fields = [
        'created',
        'date',
        'start_time',
        'end_time']
    queryset = TaskOccurrence.objects.all()  # pylint: disable=no-member
