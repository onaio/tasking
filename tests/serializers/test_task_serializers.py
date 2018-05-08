# -*- coding: utf-8 -*-
"""
Module for the Task model(s)
"""
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone
from tasking.serializers import TaskSerializer
from model_mommy import mommy


class TestTaskSerializer(TestCase):
    """
    Test the taskSerializer
    """

    def test_create(self):
        """
        Test that the serializer can create Task objects
        """
        now = timezone.now()
        mocked_target_object = mommy.make('tasking.Task')

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_type': 'task',
            'target_id': mocked_target_object.id,
            'target_app_label': 'tasking'
        }

        serializer_instance = TaskSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        # we remove this field because it is not part fo the model's
        # serialized data.  It is only used to get the content_type
        del data['target_app_label']
        # the start field is going to be converted to isformat
        data['start'] = now.isoformat()
        # import ipdb; ipdb.set_trace()
        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual('Cow price', task.name)
        self.assertEqual('Some description', task.description)
        self.assertEqual(now, task.start)
        self.assertEqual(10, task.total_submission_target)
