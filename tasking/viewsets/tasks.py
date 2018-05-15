# -*- coding: utf-8 -*-
"""
Task viewsets
"""
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.models import Task
from tasking.serializers import TaskSerializer


class TaskViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Viewset for tasks
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
