# -*- coding: utf-8 -*-
"""
Task List Serializers
"""

from __future__ import unicode_literals

from rest_framework import serializers

from tasking.models import TaskList


class TaskListSerializer(serializers.ModelSerializer):
    """
    Task List serializer class
    """
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskListSerializer
        """
        model = TaskList
        fields = [
            'id',
            'name',
            'tasks'
        ]
