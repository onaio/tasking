"""
Test for SegmentRuleSerializer
"""
from collections import OrderedDict

from tests.base import TestBase

from tasking.serializers import SegmentRuleSerializer
from tasking.utils import get_target


class TestSegmentRuleSerializer(TestBase):
    """
    Test the SegmentRuleSerializer
    """

    def test_create_segment_rule(self):
        """
        Test that the serializer can create SegmentRule objects
        """

        data = {
            "name": "Rule Zero",
            "description": "Some description",
            "target_content_type": self.task_type.id,
            "target_field": "id",
            "target_field_value": "6",
            "active": True,
        }

        task_contenttype = get_target(app_label="tasking", target_type="task")

        serializer_instance = SegmentRuleSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        segment_rule = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual("Rule Zero", segment_rule.name)
        self.assertEqual("Some description", segment_rule.description)
        self.assertEqual("id", segment_rule.target_field)
        self.assertEqual("6", segment_rule.target_field_value)
        self.assertEqual(task_contenttype, segment_rule.target_content_type)

        expected_fields = [
            "created",
            "name",
            "target_field",
            "description",
            "modified",
            "active",
            "target_content_type",
            "target_field_value",
            "id",
        ]
        self.assertEqual(set(expected_fields), set(list(serializer_instance.data)))

    def test_validate_bad_data(self):
        """
        Test validate method of SegmentRuleSerializer works as expected
        for bad data
        """

        bad_content_type = OrderedDict(
            name="Rule Zero",
            description="Some description",
            target_content_type="BAD",
            target_field="id",
            target_field_value=6,
            target_app_label="tasking",
        )

        instance = SegmentRuleSerializer(data=bad_content_type)
        self.assertFalse(instance.is_valid())

        bad_target_field = OrderedDict(
            name="Rule Zero",
            description="Some description",
            target_content_type=self.task_type.id,
            active=False,
            target_field="invalid_field",
            target_field_value=6,
            target_app_label="tasking",
        )

        instance = SegmentRuleSerializer(data=bad_target_field)
        self.assertFalse(instance.is_valid())
        self.assertEqual(
            "Task has no field named 'invalid_field'",
            instance.errors["target_field"][0],
        )
