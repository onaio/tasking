"""
Project viewsets
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.models import Project
from tasking.serializers import ProjectSerializer


# pylint: disable=too-many-ancestors
class ProjectViewSet(  # pylint: disable=bad-continuation
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    Viewset for projects
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["tasks"]
    search_fields = [
        "name",
    ]
    ordering_fields = ["name", "created"]
    queryset = Project.objects.all()  # pylint: disable=no-member
