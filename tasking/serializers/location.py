# -*- coding: utf-8 -*-
"""
Location Serializers
"""
from __future__ import unicode_literals

import zipfile

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Point

from backports.tempfile import TemporaryDirectory
from django_countries import Countries
from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from tasking.common_tags import (GEODETAILS_ONLY, GEOPOINT_MISSING,
                                 RADIUS_MISSING)
from tasking.models import Location
from tasking.utils import get_shapefile


class ShapeFileField(GeometryField):
    """
    Custom Field for Shapefile
    """

    def to_internal_value(self, value):
        """
        Custom Conversion for shapefile field
        """
        shapefile = value

        if shapefile is not None:
            try:
                zip_file = zipfile.ZipFile(value.temporary_file_path())
            except AttributeError:
                zip_file = zipfile.ZipFile(value)
            # Call get_shapefile method to get the .shp files name
            shpfile = get_shapefile(zip_file)

            # Setup a Temporary Directory to store Shapefiles
            with TemporaryDirectory() as temp_dir:
                tpath = temp_dir

                # Extract all files to Temporary Directory
                zip_file.extractall(tpath)

                # concatenate Shapefile path
                shp_path = "{tpath}/{shp}".format(tpath=tpath, shp=shpfile)

                # Make the shapefile a DataSource
                data_source = DataSource(shp_path)
                layer = data_source[0]

                # Get the first item of shapefile and turn to a Polygon Object
                shapefile = layer[1].geom.geos

        return shapefile

    def to_representation(self, value):
        """
        Custom conversion to representation for ShapeFileField
        """
        if value in ('', None):
            return ''
        return super(ShapeFileField, self).to_representation(value)


class GeopointField(GeometryField):
    """
    Custom Field for Geopoint
    """

    def to_internal_value(self, value):
        """
        Custom conversion for GeopointField
        """
        geopoint = value
        if geopoint is not None:
            geopoint_split = geopoint.split(',')
            lon = int(geopoint_split[0])
            lat = int(geopoint_split[1])

        return Point(lon, lat)

    def to_representation(self, value):
        """
        Custom conversion to representation for GeopointField
        """
        if value in ('', None):
            return ''
        return super(GeopointField, self).to_representation(value)


class SerializableCountryField(serializers.ChoiceField):
    """
    Custom Serialization for Country Field
    """

    def to_representation(self, value):
        if value in ('', None):
            return ''  # instead of `value` as Country(u'') is not serializable
        return super(SerializableCountryField, self).to_representation(value)


class LocationSerializer(serializers.ModelSerializer):
    """
    Location serializer class
    """
    country = SerializableCountryField(
        allow_blank=True, required=False, choices=Countries())

    shapefile = ShapeFileField(required=False)
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
