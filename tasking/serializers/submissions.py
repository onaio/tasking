# -*- coding: utf-8 -*-
"""
Submission Serializers
"""
from __future__ import unicode_literals

from tasking.models import Submission
from tasking.serializers.base import GenericForeignKeySerializer


class SubmissionSerializer(GenericForeignKeySerializer):
    """
    Submission serializer class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for SubmissionSerializer
        """
        fields = [
            'id',
            'created',
            'modified',
            'task',
            'location',
            'user',
            'submission_time',
            'valid',
            'approved',
            'comments',
            'target_content_type',
            'target_id',
        ]
        model = Submission
