# -*- coding: utf-8 -*-
"""
Base Serializers
"""
from __future__ import unicode_literals

from rest_framework import serializers

from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.exceptions import TargetDoesNotExist
from tasking.utils import get_target


def validate_content_type(attrs):
    """
    Helper function to validate content type
    """
    # we are checking if we have a model of this type
    target_type = attrs.get('target_content_type')
    app_label = attrs.get('target_app_label')

    try:
        target_model_contentype = get_target(
            app_label=app_label, target_type=target_type)
    except TargetDoesNotExist:
        raise serializers.ValidationError(
            {'target_type': TARGET_DOES_NOT_EXIST}
        )

    # at this point we know that the content type exists
    # next we add the contenttype object to attrs because it is
    # expected by model serializers
    attrs['target_content_type'] = target_model_contentype
    # we only needed the app label when finding the content type
    # so we remove it from attrs
    del attrs['target_app_label']

    return attrs


class ContentTypeFieldSerializer(serializers.ModelSerializer):
    """
    Serializer class that provides a contenty_type field and a method
    to validate it
    """

    target_type = serializers.CharField(
        source='target_content_type',
        allow_blank=False)
    target_app_label = serializers.CharField(
        write_only=True,
        allow_blank=False)

    def validate(self, attrs):
        """
        Custom validation for content_type field
        """

        attrs = super(ContentTypeFieldSerializer, self).validate(attrs)
        attrs = validate_content_type(attrs)

        return super(ContentTypeFieldSerializer, self).validate(attrs)


class GenericForeignKeySerializer(ContentTypeFieldSerializer):
    """
    Serializer class that provides fields and methods for dealing
    with generic foreign keys
    """

    target_id = serializers.IntegerField(source='target_object_id')

    def validate(self, attrs):
        """
        Validate target id
        """
        attrs = validate_content_type(attrs)
        target_id = attrs.get('target_object_id')
        target_model_contenttype = attrs.get('target_content_type')
        target_model_class = target_model_contenttype.model_class()

        try:
            target_model_class.objects.get(pk=target_id)
        except target_model_class.DoesNotExist:
            raise serializers.ValidationError(
                {'target_id': TARGET_DOES_NOT_EXIST}
            )

        return attrs
