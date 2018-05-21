# -*- coding: utf-8 -*-
"""
Location Serializers
"""
from __future__ import unicode_literals

from tempfile import TemporaryDirectory
import zipfile

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.serializers import GeometryField
from rest_framework import serializers
from django.contrib.gis.geos import Point
from django_countries import Countries
from django.contrib.gis.gdal import DataSource

from tasking.common_tags import RADIUS_MISSING, GEODETAILS_ONLY
from tasking.common_tags import GEOPOINT_MISSING
from tasking.models import Location
from tasking.utils import get_shpname


class ShapeFileField(GeometryField):
    """
    Custom Field for Shapefile
    """

    def to_internal_value(self, data):
        zip_file = zipfile.ZipFile(data.temporary_file_path())
        shpfile = get_shpname(zip_file)
        # Setup a Temporary Directory to store Shapefiles
        tdir = TemporaryDirectory()
        tpath = tdir.name
        # Extract all files to Temporary Directory
        zip_file.extractall(tpath)
        shp_path = tpath+'/'+shpfile

        data_source = DataSource(shp_path)
        layer = data_source[0]
        # Get the first item of shapefile and turn to WKT
        item = layer[1].geom.wkt

        return item

    def to_representation(self, value):
        if value in ('', None):
            return ''
        return super(ShapeFileField, self).to_representation(value)


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


class SerializableCountryField(serializers.ChoiceField):
    """
    Custom Serialization for Country Field
    """

    def to_representation(self, value):
        if value in ('', None):
            return ''  # instead of `value` as Country(u'') is not serializable
        return super(SerializableCountryField, self).to_representation(value)


class LocationSerializer(GeoFeatureModelSerializer):
    """
    Location serializer class
    """
    country = SerializableCountryField(
        allow_blank=True, required=False, choices=Countries())

    shapefile = ShapeFileField(required=False)

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
        geo_field = "shapefile"
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
