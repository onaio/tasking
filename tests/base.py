"""
Base Tasking test classes
"""

from django.test import TestCase

from tasking.utils import get_allowed_contenttypes


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
