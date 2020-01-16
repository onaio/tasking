"""
Submission Serializers
"""
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
            if self.instance.task == value:
                return value
            raise serializers.ValidationError(
                CANT_EDIT_TASK
            )
        return value

    # pylint: disable=too-few-public-methods
    class Meta:
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
            'status',
            'comments',
            'target_content_type',
            'target_id',
        ]
        model = Submission
