# -*- coding: utf-8 -*-
"""
Test for Project model
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy


class TestProject(TestCase):
    """
    Test class for TaskProject models
    """

    def test_project_model_str(self):
        """
        Test __str__ method of Project model
        """

        livestock_task_list = mommy.make(
            'tasking.Project',
            name="Livestock tasks")
        expected = "Livestock tasks"
        self.assertEqual(expected, livestock_task_list.__str__())
