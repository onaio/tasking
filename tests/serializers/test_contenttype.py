# -*- coding: utf-8 -*-
"""
Test for ContentTypeSerializer
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from tasking.serializers import ContentTypeSerializer


class TestContentTypeSerializer(TestCase):
    """
    Tests the ContentTypeSerializer
    """

    def test_serializer_output(self):
        """
        Test that the serializer returns the expected fields
        """
        mocked_task = mommy.make('tasking.Task')
        data = {
            'app_label': 'tasking',
            'model': 'task',
            'id': mocked_task.id,
        }

        serializer_instance = ContentTypeSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        expected_fields = {
            'app_label',
            'model',
            'id'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
