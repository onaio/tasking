# -*- coding: utf-8 -*-
"""
Tests for tasking utils
"""
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone

from dateutil.rrule import rrulestr
from dateutil.parser import parse

from tasking.exceptions import TargetDoesNotExist
from tasking.models import Task
from tasking.utils import (get_rrule_end, get_rrule_start, get_target,
                           validate_rrule)


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

    def test_get_rrule_start(self):
        """
        Test that get_rrule_start returns the rrule start correctly
        """
        # test when DTSTART is provided
        rule1 = 'DTSTART:19970902T090000 RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        start1 = get_rrule_start(rrulestr(rule1))
        # must be timezone aware
        self.assertTrue(timezone.is_aware(start1))
        # check that it matches the datetime
        expected1 = timezone.make_aware(parse("19970902T090000"))
        self.assertEqual(expected1, start1)

        # test when DTSTART is not provided
        rule2 = 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        start2 = get_rrule_start(rrulestr(rule2))
        # must be timezone aware
        self.assertTrue(timezone.is_aware(start2))
        # check that it matches today
        now = timezone.now()
        self.assertEqual(now.year, start2.year)
        self.assertEqual(now.month, start2.month)
        self.assertEqual(now.day, start2.day)
        self.assertEqual(now.hour, start2.hour)
