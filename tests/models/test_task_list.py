# -*- coding: utf-8 -*-
"""
Test for Task List model
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy


class TestTaskList(TestCase):
    """
    Test class for TaskList models
    """

    def test_task_list_model_str(self):
        livestock_task_list = mommy.make(
            'tasking.TaskList',
            name="Livestock tasks")
        expected = "Livestock tasks"
        self.assertEqual(expected, livestock_task_list.__str__())
