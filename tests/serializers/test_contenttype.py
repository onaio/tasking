# -*- coding: utf-8 -*-
"""
Test for ContentTypeSerializer
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from tasking.serializers import ContentTypeSerializer


class TestContentTypeSerializer(TestCase):
    """
    Tests the ContentTypeSerializer
    """

    def test_serializer_output(self):
        """
        Test that the serializer returns the expected fields
        """
        mocked_contenttype = ContentType.objects.filter(
            app_label='tasking', model='task').first()

        serializer_data = ContentTypeSerializer(mocked_contenttype).data

        expected_fields = {
            'app_label',
            'model',
            'id'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_data.keys())))
        self.assertEqual(
            mocked_contenttype.app_label, serializer_data['app_label'])
        self.assertEqual(mocked_contenttype.model, serializer_data['model'])
        self.assertEqual(mocked_contenttype.id, serializer_data['id'])
