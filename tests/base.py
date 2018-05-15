# -*- coding: utf-8 -*-
"""
Base Tasking test classes
"""
from __future__ import unicode_literals

from django.test import TestCase

from tasking.tools import get_allowed_contenttypes


class TestBase(TestCase):
    """
    Base test class
    """

    def setUp(self):
        """
        Setup tests
        """
        # get the content type for Task model
        self.task_type = get_allowed_contenttypes().filter(
            model='task').first()
        # get the content type for User model
        self.user_type = get_allowed_contenttypes().filter(
            model='user').first()
