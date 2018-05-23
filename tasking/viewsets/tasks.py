# -*- coding: utf-8 -*-
"""
Task viewsets
"""
from __future__ import unicode_literals

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.filters import TaskFilterSet
from tasking.models import Task
from tasking.serializers import TaskSerializer


# pylint: disable=too-many-ancestors
class TaskViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for tasks
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter]
    filter_class = TaskFilterSet
    search_fields = ['name', ]
    ordering_fields = [
        'created',
        'status',
        'submission_count',
        'project__id',
        'name'
    ]
    queryset = Task.with_submission_count.all()
