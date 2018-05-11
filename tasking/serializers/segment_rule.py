# -*- coding: utf-8 -*-
"""
SegmentRule Serializers
"""
from __future__ import unicode_literals

from tasking.models import SegmentRule
from tasking.serializers.base import ContentTypeFieldSerializer


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
            'target_content_type',
            'target_field',
            'target_field_value',
            'id',
            'created',
            'modified',
            'name',
        ]
        model = SegmentRule
