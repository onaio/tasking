"""
ContentType serializer
"""
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
            "id",
            "app_label",
            "model",
        ]
