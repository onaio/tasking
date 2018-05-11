# -*- coding: utf-8 -*-
"""
Tests for tasking tools
"""
from __future__ import unicode_literals

from django.test import TestCase

from tasking.tools import get_allowed_contenttypes
from django.contrib.contenttypes.models import ContentType


class TestTools(TestCase):
    """
    Test class for tasking tools
    """

    def test_get_allowed_contenttypes(self):
        """
        Test get_allowed_contenttypes
        """
        input_expected = [
            {'app_label': 'tasking', 'model': 'task'},
            {'app_label': 'tasking', 'model': 'segmentrule'}]

        task_type = ContentType.objects.get(app_label='tasking', model='task')
        rule_type = ContentType.objects.get(app_label='tasking',
                                            model='segmentrule')

        allowed = get_allowed_contenttypes(
            allowed_content_types=input_expected)

        self.assertEqual(2, allowed.count())
        self.assertIn(task_type, allowed)
        self.assertIn(rule_type, allowed)
