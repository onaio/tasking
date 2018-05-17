# -*- coding: utf-8 -*-
"""
Project viewsets
"""
from __future__ import unicode_literals

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.models import Project
from tasking.serializers import ProjectSerializer


# pylint: disable=too-many-ancestors
class ProjectViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for projects
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    filter_fields = ['tasks']
    search_fields = ['name', ]
    ordering_fields = ['name', 'created']
    queryset = Project.objects.all()  # pylint: disable=no-member
