# -*- coding: utf-8 -*-
"""
Location viewsets
"""
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.models import Location
from tasking.serializers import LocationSerializer


# pylint: disable=too-many-ancestors
class LocationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for Location
    """
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
