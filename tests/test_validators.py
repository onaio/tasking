# -*- coding: utf-8 -*-
"""
Tests for tasking validators
"""
from __future__ import unicode_literals

from django.test import TestCase

from tasking.validators import validate_rrule


class TestValidators(TestCase):
    """
    Test class for tasking validators
    """

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
