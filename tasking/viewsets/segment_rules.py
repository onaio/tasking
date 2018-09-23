"""
SegmentRule viewsets
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from tasking.models import SegmentRule
from tasking.serializers import SegmentRuleSerializer


# pylint: disable=too-many-ancestors
class SegmentRuleViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for segment rules
    """
    serializer_class = SegmentRuleSerializer
    permission_classes = [IsAuthenticated]
    queryset = SegmentRule.objects.all()  # pylint: disable=no-member
