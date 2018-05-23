# -*- coding: utf-8 -*-
"""
ContentType serializer
"""
from __future__ import unicode_literals

from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType


# pylint: disable=abstract-method
class ContentTypeSerializer(serializers.Serializer):
    """
    Serializer for ContentType ViewSet
    """
    app_label = serializers.CharField(max_length=255)
    model = serializers.CharField(max_length=255)
    id = serializers.IntegerField()

    class Meta(object):
        """
        Meta Options for ContentTypeSerializer
        """
        model = ContentType
        fields = [
            'app_label',
            'model',
            'id'
        ]
