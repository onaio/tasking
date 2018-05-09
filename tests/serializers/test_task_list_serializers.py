# -*- coding: utf-8 -*-
"""
Test for Task List Serializers
"""
from __future__ import unicode_literals

from django.test import TestCase

from tasking.serializers import TaskListSerializer

class TestTaskListSerializer(TestCase):
    """
    Test the Task List Serializer
    """
    def test_create_task_list(self):
        """
        Test that the serializer can create Task List objects
        """
        data = {
        'name': "Livestock prices"
        }
        serializer_instance = TaskListSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        task_list = serializer_instance.save()
        self.assertDictContainsSubset(data, serializer_instance.data)
