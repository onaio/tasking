# -*- coding: utf-8 -*-
"""
Location Serializers
"""
from __future__ import unicode_literals

from rest_framework import serializers
from django.contrib.gis.geos import Point

from tasking.common_tags import RADIUS_MISSING, GEODETAILS_ONLY
from tasking.common_tags import GEOPOINT_MISSING
from tasking.models import Location


# pylint: disable=W0223
class GeopointField(serializers.Field):
    """
    Custom Field for Geopoint
    """

    def to_internal_value(self, data):
        """
        Custom conversion for Geopoint field
        """
        geopoint = data

        if geopoint is not None:
            geopoint_split = geopoint.split(',')
            lon = int(geopoint_split[0])
            lat = int(geopoint_split[1])

        return Point(lon, lat)


class LocationSerializer(serializers.ModelSerializer):
    """
    Location serializer class
    """
    geopoint = GeopointField(required=False)

    def validate(self, attrs):
        """
        Custom Validation for Location Serializer
        """
        geopoint = attrs.get('geopoint')
        radius = attrs.get('radius')
        shapefile = attrs.get('shapefile')

        if geopoint is not None:
            if shapefile is not None:
                raise serializers.ValidationError(
                    {'shapefile': GEODETAILS_ONLY}
                )
            if radius is None:
                raise serializers.ValidationError(
                    {'radius': RADIUS_MISSING}
                )
        if radius is not None:
            if shapefile is not None:
                raise serializers.ValidationError(
                    {'shapefile': GEODETAILS_ONLY}
                )
            if geopoint is None:
                raise serializers.ValidationError(
                    {'geopoint': GEOPOINT_MISSING}
                )

        return super(LocationSerializer, self).validate(attrs)

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for LocationSerializer
        """
        model = Location
        fields = [
            'id',
            'name',
            'country',
            'geopoint',
            'radius',
            'shapefile',
            'parent',
            'created',
            'modified'
        ]
