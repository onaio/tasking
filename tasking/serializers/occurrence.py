# -*- coding: utf-8 -*-
"""
TaskOccurrence Serializers
"""

from __future__ import unicode_literals

from rest_framework import serializers

from tasking.models import TaskOccurrence


class TaskOccurrenceSerializer(serializers.ModelSerializer):
    """
    TaskOccurrence serializer class
    """
    time_string = serializers.SerializerMethodField()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for TaskOccurrenceSerializer
        """
        model = TaskOccurrence
        fields = [
            'id',
            'task',
            'location',
            'created',
            'modified',
            'date',
            'start_time',
            'end_time',
            'time_string'
        ]

    # pylint: disable=no-self-use
    def get_time_string(self, obj):
        """
        Returns a friendly human-readable description of the occurrence
        date and times
        """
        return obj.get_timestring()
