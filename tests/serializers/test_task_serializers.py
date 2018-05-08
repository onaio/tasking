# -*- coding: utf-8 -*-
"""
Module for the Task model(s)
"""
from __future__ import unicode_literals
from collections import OrderedDict

from django.test import TestCase
from django.utils import timezone
from tasking.serializers import TaskSerializer
from tasking.common_tags import TARGET_DOES_NOT_EXIST
from rest_framework.exceptions import ValidationError
from tasking.utils import get_target
from model_mommy import mommy


class TestTaskSerializer(TestCase):
    """
    Test the taskSerializer
    """

    def test_task_serializer_validate_bad_data(self):
        """
        Test validate method of TaskSerializer works as expected
        for bad data
        """
        mocked_target_object = mommy.make('tasking.Task')

        bad_target_id = OrderedDict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type='task',
            target_object_id=1337,
            target_app_label='tasking'
        )

        with self.assertRaises(ValidationError) as bad_target_id_cm:
            TaskSerializer().validate(bad_target_id)

        self.assertEqual(
            {'target_id': TARGET_DOES_NOT_EXIST},
            bad_target_id_cm.exception.args[0])
        self.assertEqual(400, bad_target_id_cm.exception.status_code)

        bad_target_app_label = OrderedDict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type='task',
            target_object_id=mocked_target_object.id,
            target_app_label='superduperapp'
        )

        with self.assertRaises(ValidationError) as bad_target_app_label_cm:
            TaskSerializer().validate(bad_target_app_label)

        self.assertEqual(
            {'target_type': TARGET_DOES_NOT_EXIST},
            bad_target_app_label_cm.exception.args[0])
        self.assertEqual(400, bad_target_app_label_cm.exception.status_code)

        bad_content_type = OrderedDict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type='foobar',
            target_object_id=mocked_target_object.id,
            target_app_label='tasking'
        )

        with self.assertRaises(ValidationError) as bad_content_type_cm:
            TaskSerializer().validate(bad_content_type)

        self.assertEqual(
            {'target_type': TARGET_DOES_NOT_EXIST},
            bad_content_type_cm.exception.args[0])
        self.assertEqual(400, bad_content_type_cm.exception.status_code)

    def test_task_serializer_validate(self):
        """
        Test validate method of TaskSerializer works as expected
        """
        now = timezone.now()
        mocked_target_object = mommy.make('tasking.Task')

        attrs = OrderedDict(
            name='Cow price',
            description='Some description',
            start=now,
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type='task',
            target_object_id=mocked_target_object.id,
            target_app_label='tasking'
        )
        validated_data = TaskSerializer().validate(attrs)

        expected_contenttype = get_target(
            app_label='tasking', target_type='task')
        expected = OrderedDict(
            name='Cow price',
            description='Some description',
            start=now,
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type=expected_contenttype,
            target_object_id=mocked_target_object.id
        )

        self.assertDictEqual(dict(expected), dict(validated_data))

    def test_create_task(self):
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

    def test_validate_timing_rule(self):
        """
        Test that the serializer timing_rule validation works
        """
        mocked_target_object = mommy.make('tasking.Task')

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': timezone.now(),
            'total_submission_target': 10,
            'timing_rule': 'inva;lid',
            'target_type': 'task',
            'target_id': mocked_target_object.id,
            'target_app_label': 'tasking'
        }

        serializer_instance = TaskSerializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
