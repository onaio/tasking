# -*- coding: utf-8 -*-
"""
Tasking Serializers
"""
from __future__ import unicode_literals

from rest_framework import serializers

from tasking.common_tags import INVALID_TIMING_RULE
from tasking.models import Task
from tasking.utils import validate_rrule
from tasking.serializers.base import GenericForeignKeySerializer


class TaskSerializer(GenericForeignKeySerializer):
    """
    Task serializer class
    """

    # pylint: disable=no-self-use
    def validate_timing_rule(self, value):
        """
        Validate timing rule
        """
        if validate_rrule(value) is True:
            return value
        raise serializers.ValidationError(
            {'timing_rule': INVALID_TIMING_RULE}
        )

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskSerializer
        """
        fields = [
            'id',
            'name',
            'parent',
            'description',
            'start',
            'end',
            'timing_rule',
            'total_submission_target',
            'user_submission_target',
            'status',
            'target_app_label',
            'target_type',
            'target_id',
            'segment_rules',
        ]
        model = Task
