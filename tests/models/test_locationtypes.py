# -*- coding: utf-8 -*-
"""
Test for LocationType model
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy


class TestLocationTypes(TestCase):
    """
    Test class for LocationType model
    """

    def test_locationtype_model_str(self):
        """
        Test the str method on LocationType model
        """
        waterfront = mommy.make(
            'tasking.LocationType',
            name="Waterfront")
        expected = 'Waterfront'
        self.assertEqual(expected, waterfront.__str__())
