"""
Project viewsets
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.models import LocationType
from tasking.serializers import LocationTypeSerializer


# pylint: disable=too-many-ancestors
class LocationTypeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for LocationTypes
    """
    serializer_class = LocationTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = LocationType.objects.all()  # pylint: disable=no-member
