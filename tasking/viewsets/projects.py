# -*- coding: utf-8 -*-
"""
Project viewsets
"""
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
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
    queryset = Project.objects.all()  # pylint: disable=no-member
