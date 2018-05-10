# -*- coding: utf-8 -*-
"""
Test for SegmentRuleSerializer
"""
from __future__ import unicode_literals

from collections import OrderedDict

from django.test import TestCase
from django.utils import six

from rest_framework.exceptions import ValidationError

from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.serializers import SegmentRuleSerializer
from tasking.utils import get_target


class TestSegmentRuleSerializer(TestCase):
    """
    Test the SegmentRuleSerializer
    """

    def test_create_segment_rule(self):
        """
        Test that the serializer can create SegmentRule objects
        """

        data = {
            'name': 'Rule Zero',
            'description': 'Some description',
            'target_type': 'task',
            'target_app_label': 'tasking',
            'target_field': 'id',
            'target_field_value': '6',
            'active': True
        }

        task_contenttype = get_target(
            app_label='tasking', target_type='task')

        serializer_instance = SegmentRuleSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        segment_rule = serializer_instance.save()

        # we remove this field because it is not part fo the model's
        # serialized data.  It is only used to get the content_type
        del data['target_app_label']
        # the start field is going to be converted to isformat
        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual('Rule Zero', segment_rule.name)
        self.assertEqual('Some description', segment_rule.description)
        self.assertEqual('id', segment_rule.target_field)
        self.assertEqual('6', segment_rule.target_field_value)
        self.assertEqual(task_contenttype, segment_rule.target_content_type)

        expected_fields = [
            'created',
            'name',
            'target_field',
            'description',
            'modified',
            'active',
            'target_type',
            'target_field_value',
            'id',
        ]

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data)))

    def test_segment_rule_validate(self):
        """
        Test validate method of SegmentRuleSerializer works as expected
        """

        attrs = OrderedDict(
            name='Rule Zero',
            description='Some description',
            target_content_type='task',
            target_field='id',
            target_field_value=6,
            target_app_label='tasking'
        )
        validated_data = SegmentRuleSerializer().validate(attrs)

        expected_contenttype = get_target(
            app_label='tasking', target_type='task')
        expected = OrderedDict(
            name='Rule Zero',
            description='Some description',
            target_content_type=expected_contenttype,
            target_field='id',
            target_field_value=6
        )
        self.assertDictEqual(dict(expected), dict(validated_data))

    def test_validate_bad_data(self):
        """
        Test validate method of SegmentRuleSerializer works as expected
        for bad data
        """

        bad_target_app_label = OrderedDict(
            name='Rule Zero',
            description='Some description',
            target_content_type='task',
            target_field='id',
            target_field_value=6,
            target_app_label='BAD'
        )

        with self.assertRaises(ValidationError) as bad_target_app_label_cm:
            SegmentRuleSerializer().validate(bad_target_app_label)

        error_detail = bad_target_app_label_cm.exception.detail['target_type']
        self.assertEqual(TARGET_DOES_NOT_EXIST, six.text_type(error_detail))
        self.assertEqual('invalid', error_detail.code)
        self.assertEqual(400, bad_target_app_label_cm.exception.status_code)

        bad_content_type = OrderedDict(
            name='Rule Zero',
            description='Some description',
            target_content_type='BAD',
            target_field='id',
            target_field_value=6,
            target_app_label='tasking'
        )

        with self.assertRaises(ValidationError) as bad_content_type_cm:
            SegmentRuleSerializer().validate(bad_content_type)

        error_detail = bad_content_type_cm.exception.detail['target_type']
        self.assertEqual(TARGET_DOES_NOT_EXIST, six.text_type(error_detail))
        self.assertEqual('invalid', error_detail.code)
        self.assertEqual(400, bad_content_type_cm.exception.status_code)
