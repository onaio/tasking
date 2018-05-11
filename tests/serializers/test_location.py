# -*- coding: utf-8 -*-
"""
Tests for LocationSerializer
"""
from __future__ import unicode_literals

from collections import OrderedDict

from django.test import TestCase
from django.utils import six

from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError
from model_mommy import mommy

from tasking.serializers import LocationSerializer
from tasking.common_tags import RADIUS_MISSING, GEOPOINT_MISSING
from tasking.common_tags import GEODETAILS_ONLY


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
            'country': 'KE',
            }
        serializer_instance = LocationSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        location = serializer_instance.save()

        self.assertEqual('Nairobi', location.name)
        self.assertEqual('KE', location.country)
        self.assertEqual('Kenya - Nairobi', six.text_type(location))

        expected_fields = [
            'created',
            'name',
            'modified',
            'country',
            'shapefile',
            'geopoint',
            'id',
            'radius'
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data)))

    def test_validate_bad_data(self):
        """
        Test validate method of LocationSerializer works as expected
        for bad data
        """
        mocked_location_with_shapefile = mommy.make(
            'tasking.Location',
            name='Nairobi',
            _fill_optional=['shapefile'])
        missing_radius = OrderedDict(
            name='Nairobi',
            geopoint='Point(0.0, 0.0)')
        missing_geopoint = OrderedDict(
            name='Montreal',
            radius=45.678)
        shapefile_radius = OrderedDict(
            name='Arusha',
            radius=56.6789,
            geopoint='Point(0.0, 0.0)',
            shapefile=mocked_location_with_shapefile.shapefile)

        with self.assertRaises(ValidationError) as missing_radius_cm:
            LocationSerializer().validate(missing_radius)

        radius_error_detail = missing_radius_cm.exception.detail['radius']
        self.assertEqual(RADIUS_MISSING, six.text_type(radius_error_detail))

        with self.assertRaises(ValidationError) as missing_geopoint_cm:
            LocationSerializer().validate(missing_geopoint)

        geopnt_error_detail = missing_geopoint_cm.exception.detail['geopoint']
        self.assertEqual(GEOPOINT_MISSING, six.text_type(geopnt_error_detail))

        with self.assertRaises(ValidationError) as shapefile_radius_cm:
            LocationSerializer().validate(shapefile_radius)

        shape_error_detail = shapefile_radius_cm.exception.detail['shapefile']
        self.assertEqual(GEODETAILS_ONLY, six.text_type(shape_error_detail))

    def test_location_serializer_validate_shapefile(self):
        """
        Test validate method of TaskSerializer works as expected for shapefile
        """
        mocked_location_with_shapefile = mommy.make(
            'tasking.Location',
            name='Nairobi',
            _fill_optional=['shapefile'])
        data = OrderedDict(
            name='Montreal',
            shapefile=mocked_location_with_shapefile.shapefile)

        validated_data = LocationSerializer().validate(data)
        self.assertDictEqual(dict(data), dict(validated_data))

    def test_location_serializer_validate_geodetails(self):
        """
        Test validate method of TaskSerializer works as expecter for
        geopoint and radius
        """
        point = Point(0.0, 0.0)
        data = OrderedDict(
            name='Spain',
            geopoint=point,
            radius=45.986,
            )
        validated_data = LocationSerializer().validate(data)
        self.assertDictEqual(dict(data), dict(validated_data))
