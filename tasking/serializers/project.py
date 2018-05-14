# -*- coding: utf-8 -*-
"""
Project Serializers
"""

from __future__ import unicode_literals

from rest_framework import serializers

from tasking.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Project serializer class
    """
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for ProjectSerializer
        """
        model = Project
        fields = [
            'id',
            'name',
            'tasks',
            'created',
            'modified'
        ]
