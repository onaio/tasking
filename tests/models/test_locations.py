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
        Test the str method on Location model with Country Defined
        """
        nairobi = mommy.make(
            'tasking.Location',
            name="Nairobi",
            country="KE")
        expected = 'Kenya - Nairobi'
        self.assertEqual(expected, nairobi.__str__())

    def test_task_model_str_no_country(self):
        """
        Test the str method on Location model without Country Defined
        """
        nairobi = mommy.make('tasking.Location', name="Nairobi")
        expected = 'Nairobi'
        self.assertEqual(expected, nairobi.__str__())

    def test_entry_geodetails(self):
        """
        Test when geopoint or a radius is entered the other is present and
        Only Geopoint and Radius Or Shapefile are entered not both
        """
        mocked_geodetails = mommy.make(
            'tasking.Location',
            geopoint='POINT(0.0 0.0)',
            radius=45.678)

        if mocked_geodetails.shapefile is not None:
            self.assertEqual(None, mocked_geodetails.geopoint)
            self.assertEqual(None, mocked_geodetails.radius)
        elif mocked_geodetails.geopoint is not None:
            self.assertTrue(mocked_geodetails.radius is not None)
            self.assertEqual(None, mocked_geodetails.shapefile)
        elif mocked_geodetails.radius is not None:
            self.assertTrue(mocked_geodetails.radius is not None)
            self.assertEqual(None, mocked_geodetails.shapefile)
        else:
            self.assertEqual(None, mocked_geodetails.geopoint)
            self.assertEqual(None, mocked_geodetails.radius)
            self.assertEqual(None, mocked_geodetails.shapefile)
