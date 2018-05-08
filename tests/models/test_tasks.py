# -*- coding: utf-8 -*-
"""
Module for the Task model(s)
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy


class TestUtils(TestCase):
    """
    Test class for tasking utils
    """

    def test_task_model_str(self):
        cow_price = mommy.make('tasking.Task', name="Cow prices")
        expected = 'Cow prices - {}'.format(cow_price.pk)
        self.assertEqual(expected, cow_price.__str__())
