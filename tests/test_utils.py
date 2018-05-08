# -*- coding: utf-8 -*-
"""
Tests for tasking utils
"""
from __future__ import unicode_literals

from tasking.utils import validate_rrule, get_target
from tasking.exceptions import TargetDoesNotExist
from tasking.models import Task
from django.test import TestCase


class TestUtils(TestCase):
    """
    Test class for tasking utils
    """

    def test_get_target(self):
        """
        Test get_target
        """
        # check that we can get a content type corectly
        task_contenttype = get_target(app_label='tasking', target_type='task')
        self.assertEqual(task_contenttype.model_class(), Task)
        # check that we get TargetDoesNotExist when the content type does
        # not exist
        with self.assertRaises(TargetDoesNotExist):
            get_target(app_label='foo', target_type='bar')

    def test_validate_rrule(self):
        """
        Test validate_rrule
        """
        # test that a valid rrule works
        self.assertTrue(validate_rrule("RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5"))
        # test that invalid rrules return False
        self.assertFalse(validate_rrule(1337))
        self.assertFalse(validate_rrule({}))
        self.assertFalse(validate_rrule([]))
        self.assertFalse(validate_rrule((12, 23)))
        self.assertFalse(validate_rrule("SELECT * FROM auth_user;"))
        self.assertFalse(validate_rrule("random string"))
