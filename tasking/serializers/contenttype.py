# -*- coding: utf-8 -*-
"""
ContentType serializer
"""
from __future__ import unicode_literals

from rest_framework import serializers


# pylint: disable=abstract-method
class ContentTypeSerializer(serializers.Serializer):
    """
    Serializer for ContentType ViewSet
    """
    name = serializers.CharField(read_only=True, max_length=255)
