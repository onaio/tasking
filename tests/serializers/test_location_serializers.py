# -*- coding: utf-8 -*-
"""
Tests for LocationSerializer
"""
from __future__ import unicode_literals

from django.test import TestCase

from tasking.serializers import LocationSerializer


class TestLocationSerializer(TestCase):
    """
    Test the LocationSerializer
    """

    def test_location_create(self):
        """
        Test that the serializer can create Location Objects
        """

        data = {
            'name': 'Nairobi',
            'country': 'KE'}

        serializer_instance = LocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        location = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual('Nairobi', location.name)
        self.assertEqual('Kenya', location.country.name)
