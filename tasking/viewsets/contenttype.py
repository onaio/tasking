"""
ContentType viewsets
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.utils import get_allowed_contenttypes
from tasking.serializers import ContentTypeSerializer


# pylint: disable=too-many-ancestors
class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Viewset for ContentType
    """
    serializer_class = ContentTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = get_allowed_contenttypes()

    def get_queryset(self):
        queryset = super(ContentTypeViewSet, self).get_queryset()
        return queryset.order_by('app_label', 'model')
