# -*- coding: utf-8 -*-
"""
SegmentRule Serializers
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.utils import six

from rest_framework.serializers import ValidationError

from tasking.common_tags import TARGET_DOES_NOT_EXIST
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

    def validate(self, attrs):
        """
        Custom validation for SegmentRuleSerializer
        """

        # validate that target_field is actually an existing field
        # on the target model
        if self.instance is None:
            target_field = attrs.get('target_field')
            target_type = attrs.get('target_content_type')
        else:
            # in this case we are editting an existing record
            target_field = attrs.get(
                'target_field', self.instance.target_field)
            target_type = attrs.get(
                'target_content_type', self.instance.target_content_type)

        if not target_type or not isinstance(target_type, ContentType):
            raise ValidationError({
                'target_content_type': TARGET_DOES_NOT_EXIST
            })
        target_model = target_type.model_class()

        try:
            # pylint: disable=protected-access
            target_model._meta.get_field(target_field)
        except FieldDoesNotExist as exception:
            raise ValidationError({
                'target_field': six.text_type(exception)
            })

        return super(SegmentRuleSerializer, self).validate(attrs)
