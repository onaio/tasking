# -*- coding: utf-8 -*-
"""
Submission viewsets
"""
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
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
    queryset = Submission.objects.all()  # pylint: disable=no-member
