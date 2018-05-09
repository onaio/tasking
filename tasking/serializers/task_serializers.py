# -*- coding: utf-8 -*-
"""
Tasking Serializers
"""
from __future__ import unicode_literals

from rest_framework import serializers

from tasking.common_tags import INVALID_TIMING_RULE, TARGET_DOES_NOT_EXIST
from tasking.exceptions import TargetDoesNotExist
from tasking.models import Task
from tasking.utils import get_target, validate_rrule


class TaskSerializer(serializers.ModelSerializer):
    """
    Task serializer class
    """

    target_id = serializers.IntegerField(source='target_object_id')
    target_type = serializers.CharField(
        source='target_content_type',
        allow_blank=False)
    target_app_label = serializers.CharField(
        write_only=True,
        allow_blank=False)

    # pylint: disable=no-self-use
    def validate_timing_rule(self, value):
        """
        Validate timing rule
        """
        if validate_rrule(value) is True:
            return value
        raise serializers.ValidationError({'timing_rule': INVALID_TIMING_RULE})

    def validate(self, attrs):
        """
        Custom validation for TaskSerializer
        """

        target_id = attrs.get('target_object_id')
        target_type = attrs.get('target_content_type')
        app_label = attrs.get('target_app_label')

        # we are checking if we have a model of this type
        try:
            target_model_contentype = get_target(
                app_label=app_label,
                target_type=target_type)
        except TargetDoesNotExist:
            raise serializers.ValidationError(
                {'target_type': TARGET_DOES_NOT_EXIST}
            )
        else:
            target_model_class = target_model_contentype.model_class()

        # now that we have the model, we need to check if there is an object
        # of that model with the supplied target_id
        try:
            target_model_class.objects.get(pk=target_id)
        except target_model_class.DoesNotExist:
            raise serializers.ValidationError(
                {'target_id': TARGET_DOES_NOT_EXIST}
            )

        # this field needs to refer to the content type object so we add
        # it to attrs
        attrs['target_content_type'] = target_model_contentype
        # we only needed the app label when finding the content type
        # so we remove it from data
        del attrs['target_app_label']
        # these attrs are then passed on to the create method of the
        # ModelSerializer
        return super(TaskSerializer, self).validate(attrs)

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
            'task_list_id',
            'start',
            'end',
            'timing_rule',
            'total_submission_target',
            'user_submission_target',
            'status',
            'target_app_label',
            'target_type',
            'target_id'
        ]
        model = Task
