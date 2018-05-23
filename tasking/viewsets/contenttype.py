# -*- coding: utf-8 -*-
"""
ContentType viewsets
"""
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.tools import get_allowed_contenttypes
from tasking.serializers import ContentTypeSerializer


# pylint: disable=too-many-ancestors
class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Viewset for ContentType
    """
    serializer_class = ContentTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = get_allowed_contenttypes()

    def filter_queryset(self, queryset):
        # Order output of ViewSet
        queryset = super(ContentTypeViewSet, self).filter_queryset(queryset)
        return queryset.order_by('model')
