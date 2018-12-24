"""
Location Serializers
"""
import zipfile
from io import BytesIO

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Point

from tempfile import TemporaryDirectory
from django_countries import Countries
from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from tasking.common_tags import (GEODETAILS_ONLY, GEOPOINT_MISSING,
                                 RADIUS_MISSING)
from tasking.exceptions import (MissingFiles, ShapeFileNotFound,
                                UnnecessaryFiles)
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
        if isinstance(value, dict):
            # if given a raw binary data buffer i.e an ArrayBuffer,
            # store the binary data in value
            # The values dict should be an ordered dict
            value = BytesIO(bytes(value.values()))

        multipolygon = value

        if multipolygon is not None:
            # open zipfile given : path to a file (a string),
            # a file-like object or a path-like object
            try:
                zip_file = zipfile.ZipFile(value.temporary_file_path())
            except AttributeError:
                zip_file = zipfile.ZipFile(value)

            # Call get_shapefile method to get the .shp files name
            try:
                shpfile = get_shapefile(zip_file)
            except (ShapeFileNotFound, MissingFiles, UnnecessaryFiles) as exp:
                # pylint: disable=no-member
                raise serializers.ValidationError(exp.message)

            # Setup a Temporary Directory to store Shapefiles
            with TemporaryDirectory() as temp_dir:
                tpath = temp_dir

                # Extract all files to Temporary Directory
                zip_file.extractall(tpath)

                # concatenate Shapefile path
                shp_path = f'{tpath}/{shpfile}'

                # Make the shapefile a DataSource
                data_source = DataSource(shp_path)
                layer = data_source[0]

                # Get geoms for all Polygons in Datasource
                polygon_data = layer.get_geoms()
                polygons = []

                for polygon in polygon_data:
                    polygons.append(polygon.geos)

                multipolygon = MultiPolygon(polygons)

        return multipolygon

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
            if isinstance(geopoint, str):
                geopoint_split = geopoint.split(',')
                lon = float(geopoint_split[0])
                lat = float(geopoint_split[1])

                return Point(lon, lat)

            if isinstance(geopoint, list):
                lon = float(geopoint[0])
                lat = float(geopoint[1])

                return Point(lon, lat)

        return super(GeopointField, self).to_internal_value(value)

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
        """
        Custom conversion to representation for Country Field
        """
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
        if self.instance:
            geopoint = attrs.get('geopoint', self.instance.geopoint)
            radius = attrs.get('radius', self.instance.radius)
            shapefile = attrs.get('shapefile', self.instance.shapefile)
        else:
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
    class Meta:
        """
        Meta options for LocationSerializer
        """
        model = Location
        fields = [
            'id',
            'name',
            'country',
            'description',
            'geopoint',
            'radius',
            'location_type',
            'shapefile',
            'parent',
            'created',
            'modified'
        ]
