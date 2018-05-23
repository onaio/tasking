# -*- coding: utf-8 -*-
"""
ContentType serializer
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for ContentType ViewSet
    """
    id = serializers.IntegerField()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta Options for ContentTypeSerializer
        """
        model = ContentType
        fields = [
            'id',
            'app_label',
            'model',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=ContentType.objects.all(),
                fields=('app_label', 'model', 'id')
            )
        ]
