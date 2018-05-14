# -*- coding: utf-8 -*-
"""
Test for Project Serializers
"""
from __future__ import unicode_literals

from collections import OrderedDict

from model_mommy import mommy
from tests.serializers.test_base import TestSerializerBase

from tasking.serializers import ProjectSerializer


class TestProjectSerializer(TestSerializerBase):
    """
    Test the Project Serializer
    """

    def test_validate_bad_data(self):
        """
        Test that ProjectSerializer validate works as expected
        for bad data.
        """
        mocked_target_object = mommy.make('tasking.Task')

        bad_target_id = OrderedDict(
            name='Livestock Prices',
            target_content_type=self.task_type.id,
            target_object_id=1337,
        )

        self.assertFalse(ProjectSerializer(data=bad_target_id).is_valid())

        bad_content_type = OrderedDict(
            name='Livestock Prices',
            target_content_type='foobar',
            target_object_id=mocked_target_object.id,
        )

        self.assertFalse(ProjectSerializer(data=bad_content_type).is_valid())

    def test_create_project(self):
        """
        Test that the serializer can create Project objects
        """

        task_1 = mommy.make('tasking.Task')
        task_2 = mommy.make('tasking.Task')
        mocked_target_object = mommy.make('tasking.Task')

        data = {
            'name': "Livestock prices",
            'target_content_type': self.task_type.id,
            'target_id': mocked_target_object.id,
        }

        data_with_tasks = data.copy()
        data_with_tasks['tasks'] = [task_1.id, task_2.id]

        serializer_instance = ProjectSerializer(data=data_with_tasks)
        self.assertTrue(serializer_instance.is_valid())
        project = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual('Livestock prices', project.name)

        self.assertEqual(set([task_1.id, task_2.id]),
                         set(serializer_instance.data['tasks']))

        expected_fields = [
            'id',
            'name',
            'tasks',
            'created',
            'modified',
            'target_content_type',
            'target_id',
        ]

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
