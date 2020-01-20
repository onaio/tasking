"""
Task viewsets
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.filters import TaskFilterSet, TaskOccurenceFilter
from tasking.models import Task
from tasking.serializers import TaskSerializer


# pylint: disable=too-many-ancestors
class TaskViewSet(  # pylint: disable=bad-continuation
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for tasks
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
        TaskOccurenceFilter,
    ]
    filterset_class = TaskFilterSet
    search_fields = [
        "name",
    ]
    ordering_fields = [
        "created",
        "status",
        "estimated_time",
        "submission_count",
        "project__id",
        "name",
    ]
    queryset = Task.with_submission_count.all()
