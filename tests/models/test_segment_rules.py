"""
Test for SegmentRule models
"""
from django.test import TestCase

from model_mommy import mommy


class TestSegmentRule(TestCase):
    """
    Test class for SegmentRule models
    """

    def test_segment_rule_model_str(self):
        """
        Test the str method on SegmentRule model
        """
        rule0 = mommy.make('tasking.SegmentRule', name='Rule Zero')
        self.assertEqual('Rule Zero', rule0.__str__())
