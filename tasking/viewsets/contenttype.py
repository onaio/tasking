"""
ContentType viewsets
"""
from django.db.models.query import QuerySet

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.serializers import ContentTypeSerializer
from tasking.utils import get_allowed_contenttypes


# pylint: disable=too-many-ancestors
class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Viewset for ContentType
    """

    serializer_class = ContentTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = get_allowed_contenttypes()

    def get_queryset(self) -> QuerySet:
        queryset = super(ContentTypeViewSet, self).get_queryset()
        return queryset.order_by("app_label", "model")
