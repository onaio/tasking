# -*- coding: utf-8 -*-
"""
Tests for LocationSerializer
"""
from __future__ import unicode_literals

from django.test import TestCase

from django.contrib.gis.geos import Point

from tasking.serializers import LocationSerializer


class TestLocationSerializer(TestCase):
    """
    Test the LocationSerializer
    """

    def test_location_create(self):
        """
        Test that the serializer can create Location Objects
        """
        point = Point(0.0, 0.0)
        data = {
            'name': 'Nairobi',
            'country': 'KE',
            'geopoint': point,
            'radius': 45.986,
            }
        serializer_instance = LocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        location = serializer_instance.save()

        self.assertEqual('Nairobi', location.name)
        self.assertEqual('KE', location.country)
        self.assertEqual(point, location.geopoint)
        self.assertEqual(45.986, float(location.radius))
