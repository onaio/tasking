# -*- coding: utf-8 -*-
"""
Location Serializers
"""
from __future__ import unicode_literals

from rest_framework import serializers

from tasking.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """
    Location serializer class
    """
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskSerializer
        """
        model = Location
        fields = [
            'id',
            'name',
            'country',
            'geopoint',
            'radius',
            'shapefile',
        ]
