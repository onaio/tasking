# -*- coding: utf-8 -*-
"""
Task List Serializers
"""

from __future__ import unicode_literals

from tasking.models import TaskList

from rest_framework import serializers

class TaskListSerializer(serializers.ModelSerializer):
    """
    Task List serializer class
    """

    class Meta(object):
        """
        Meta options for TaskListSerializer
        """
        model = TaskList
        fields = [
        'id',
        'name'
        ]
