"""
Submission viewsets
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticated

from tasking.models import Submission
from tasking.serializers import SubmissionSerializer


# pylint: disable=too-many-ancestors
class SubmissionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for submission
    """
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter,
                       DjangoFilterBackend]
    filter_fields = [
        'location',
        'task',
        'valid',
        'status',
        'user']
    search_fields = ['task__name']
    ordering_fields = [
        'created',
        'valid',
        'status',
        'submission_time',
        'task__id']
    queryset = Submission.objects.all()  # pylint: disable=no-member
