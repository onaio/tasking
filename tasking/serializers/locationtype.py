"""
LocationType serializer
"""
from __future__ import unicode_literals

from rest_framework import serializers

from tasking.models import LocationType


class LocationTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for LocationType
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta Options for LocationTypeSerializer
        """
        model = LocationType
        fields = [
            'id',
            'name',
        ]
