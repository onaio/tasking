# -*- coding: utf-8 -*-
"""
Tests for tasking exceptions
"""
from __future__ import unicode_literals

from django.test import TestCase

from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.exceptions import TargetDoesNotExist
from tasking.utils import get_target


class TestExceptions(TestCase):
    """
    Test class for tasking exceptions
    """

    def test_target_does_not_exist(self):
        """
        Test TargetDoesNotExist error message is what we expect
        """
        with self.assertRaises(TargetDoesNotExist) as context:
            get_target(app_label='foo', target_type='bar')
        the_exception = context.exception
        self.assertEqual(TARGET_DOES_NOT_EXIST, the_exception.message)
