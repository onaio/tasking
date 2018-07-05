# -*- coding: utf-8 -*-
"""
Test for TaskOccurrenceSerializer
"""
from __future__ import unicode_literals

from model_mommy import mommy
from tests.base import TestBase

from tasking.serializers import TaskOccurrenceSerializer


class TestTaskOccurrenceSerializer(TestBase):
    """
    Test the TaskOccurrenceSerializer
    """

    def test_create_occurrence(self):
        """
        Test that the serializer can create TaskOccurrence objects
        """

        task = mommy.make('tasking.Task')

        data = {
            'task': task.id,
            'date': '2018-05-24',
            'start_time': '07:00:00',
            'end_time': '19:00:00'
        }

        serializer_instance = TaskOccurrenceSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        occurrence = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual(
            occurrence.task.id, serializer_instance.data['task'])
        self.assertEqual(
            '24th May 2018, 7 a.m. to 7 p.m.',
            serializer_instance.data['time_string'])

        expected_fields = [
            'created',
            'modified',
            'task',
            'location',
            'start_time',
            'date',
            'end_time',
            'time_string',
            'id',
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data)))

    def test_occurrence_location(self):
        """
        Test occurrence creation with location
        """
        task = mommy.make('tasking.Task')
        location = mommy.make('tasking.Location')
        data = {
            'task': task.id,
            'location': location.id,
            'date': '2018-05-24',
            'start_time': '07:00:00',
            'end_time': '19:00:00'
        }

        serializer_instance = TaskOccurrenceSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        occurrence = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)

        self.assertEqual(
            occurrence.task.id, serializer_instance.data['task'])
        self.assertEqual(
            occurrence.location.id, serializer_instance.data['location'])
        self.assertEqual(
            '24th May 2018, 7 a.m. to 7 p.m.',
            serializer_instance.data['time_string'])
