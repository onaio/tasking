# -*- coding: utf-8 -*-
"""
Submission Serializers
"""
from __future__ import unicode_literals

from rest_framework import serializers

from tasking.models import Submission
from tasking.serializers.base import GenericForeignKeySerializer
from tasking.common_tags import CANT_EDIT_TASK


class SubmissionSerializer(GenericForeignKeySerializer):
    """
    Submission serializer class
    """

    def validate_task(self, value):
        """
        Validate Task
        """
        if self.instance is not None:
            if self.instance.task is value:
                return value
            else:
                raise serializers.ValidationError(
                    CANT_EDIT_TASK
                )
        else:
            return value

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for SubmissionSerializer
        """
        fields = [
            'id',
            'modified',
            'created',
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
