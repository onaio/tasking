# -*- coding: utf-8 -*-
"""
ContentType serializer
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for ContentType ViewSet
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta Options for ContentTypeSerializer
        """
        model = ContentType
        fields = [
            'id',
            'app_label',
            'model',
        ]
