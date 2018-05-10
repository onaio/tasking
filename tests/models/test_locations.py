# -*- coding: utf-8 -*-
"""
Test for Location model
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy


class TestLocations(TestCase):
    """
    Test class for Location models
    """

    def test_task_model_str(self):
        """
        Test the str method on Location model
        """
        nairobi = mommy.make('tasking.Location', name="Nairobi")
        expected = '{} - Nairobi'.format(nairobi.country.name)
        self.assertEqual(expected, nairobi.__str__())
