# -*- coding: utf-8 -*-
"""
SegmentRule Serializers
"""
from __future__ import unicode_literals

from tasking.serializers.base import ContentTypeFieldSerializer
from tasking.models import SegmentRule


class SegmentRuleSerializer(ContentTypeFieldSerializer):
    """
    SegmentRule serializer class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for SegmentRuleSerializer
        """
        fields = [
            'description',
            'active',
            'target_app_label',
            'target_type',
            'target_field',
            'target_field_value',
            'id',
            'created',
            'modified',
            'name',
        ]
        model = SegmentRule
