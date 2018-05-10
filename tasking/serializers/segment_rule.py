# -*- coding: utf-8 -*-
"""
SegmentRule Serializers
"""
from __future__ import unicode_literals

from tasking.serializers.base import GenericForeignKeySerializer
from tasking.models import SegmentRule


class SegmentRuleSerializer(GenericForeignKeySerializer):
    """
    SegmentRule serializer class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for SegmentRuleSerializer
        """
        fields = [
            'id',
            'created',
            'modified',
            'name',
            'description',
            'active',
            'target_app_label',
            'target_field',
            'target_field_value'
        ]
        model = SegmentRule
