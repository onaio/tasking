# -*- coding: utf-8 -*-
"""
Test for Project Serializers
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from tasking.serializers import ProjectSerializer


class TestProjectSerializer(TestCase):
    """
    Test the Project Serializer
    """
    def test_create_Project(self):
        """
        Test that the serializer can create Project objects
        """

        task_1 = mommy.make('tasking.Task')
        task_2 = mommy.make('tasking.Task')

        data = {'name': "Livestock prices"}
        data_with_tasks = data.copy()
        data_with_tasks['tasks'] = [task_1.id, task_2.id]

        serializer_instance = ProjectSerializer(data=data_with_tasks)

        self.assertTrue(serializer_instance.is_valid())
        Project = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual('Livestock prices', Project.name)

        self.assertEqual(set([task_1.id, task_2.id]),
                         set(serializer_instance.data['tasks']))

        expected_fields = [
            'id',
            'name',
            'tasks',
            'created',
            'modified'
        ]

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
