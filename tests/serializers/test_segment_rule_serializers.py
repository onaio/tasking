# -*- coding: utf-8 -*-
"""
Test for SegmentRuleSerializer
"""
from __future__ import unicode_literals

from collections import OrderedDict

from django.test import TestCase

from tasking.serializers import SegmentRuleSerializer
from tasking.utils import get_target

from tasking.tools import get_allowed_contenttypes


class TestSegmentRuleSerializer(TestCase):
    """
    Test the SegmentRuleSerializer
    """

    def setUp(self):
        """
        Setup tests
        """

        self.task_type = get_allowed_contenttypes().filter(
            model='task').first()

    def test_create_segment_rule(self):
        """
        Test that the serializer can create SegmentRule objects
        """

        data = {
            'name': 'Rule Zero',
            'description': 'Some description',
            'target_content_type': self.task_type.id,
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
        # del data['target_app_label']
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
            'target_content_type',
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
            target_content_type=self.task_type.id,
            target_field='id',
            target_field_value=6,
        )
        validated_data = SegmentRuleSerializer().validate(attrs)

        expected_contenttype = get_target(
            app_label='tasking', target_type='task')
        expected = OrderedDict(
            name='Rule Zero',
            description='Some description',
            target_content_type=expected_contenttype.id,
            target_field='id',
            target_field_value=6
        )
        self.assertDictEqual(dict(expected), dict(validated_data))

    def test_validate_bad_data(self):
        """
        Test validate method of SegmentRuleSerializer works as expected
        for bad data
        """

        bad_content_type = OrderedDict(
            name='Rule Zero',
            description='Some description',
            target_content_type='BAD',
            target_field='id',
            target_field_value=6,
            target_app_label='tasking'
        )

        instance = SegmentRuleSerializer(data=bad_content_type)
        self.assertFalse(instance.is_valid())
