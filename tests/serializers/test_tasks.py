# -*- coding: utf-8 -*-
"""
Test for TaskSerializer
"""
from __future__ import unicode_literals

from collections import OrderedDict

from django.utils import timezone

from model_mommy import mommy
from tests.serializers.test_base import TestSerializerBase

from tasking.serializers import TaskSerializer


class TestTaskSerializer(TestSerializerBase):
    """
    Test the TaskSerializer
    """

    def test_validate_bad_data(self):
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

        self.assertFalse(TaskSerializer(data=bad_target_id).is_valid())

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

        self.assertFalse(TaskSerializer(data=bad_content_type).is_valid())

    def test_create_task(self):
        """
        Test that the serializer can create Task objects
        """
        now = timezone.now()
        mocked_target_object = mommy.make('tasking.Task')

        rule1 = mommy.make('tasking.SegmentRule')
        rule2 = mommy.make('tasking.SegmentRule')

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.task_type.id,
            'target_id': mocked_target_object.id,
        }

        data_with_segment_rules = data.copy()
        data_with_segment_rules['segment_rules'] = [rule1.id, rule2.id]

        serializer_instance = TaskSerializer(data=data_with_segment_rules)
        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        # the start field is going to be converted to isformat
        data['start'] = now.isoformat()

        # the order of segment_rules may have changed so a dict comparison
        # may faile, we use `data` that does not include segment rules
        self.assertDictContainsSubset(data, serializer_instance.data)

        # we test that we do have our segment rules
        self.assertEqual(set([rule1.id, rule2.id]),
                         set(serializer_instance.data['segment_rules']))

        self.assertEqual('Cow price', task.name)
        self.assertEqual('Some description', task.description)
        self.assertEqual(now, task.start)
        self.assertEqual(10, task.total_submission_target)

        # test that the segment rules for the task are as we expect
        self.assertEqual(rule1, task.segment_rules.get(id=rule1.id))
        self.assertEqual(rule2, task.segment_rules.get(id=rule2.id))

        expected_fields = [
            'id',
            'created',
            'modified',
            'name',
            'parent',
            'description',
            'start',
            'end',
            'timing_rule',
            'total_submission_target',
            'user_submission_target',
            'status',
            'target_content_type',
            'target_id',
            'segment_rules',
            'location',
        ]
        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))

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

    def test_location_link(self):
        """
        Test the connection of Task and Location
        """
        location = mommy.make('tasking.location', name='Nairobi', country='KE')
        mocked_target_object = mommy.make('tasking.Task')

        now = timezone.now()

        data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'location': location.id,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.task_type.id,
            'target_id': mocked_target_object.id,
        }
        data_with_location = data.copy()
        data_with_location['location'] = [location.id]

        serializer_instance = TaskSerializer(data=data_with_location)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        self.assertEqual(location, task.location.get(id=location.id))

    def test_task_parent_link(self):
        """
        Test the connection between a parent and child task
        """
        mocked_parent_task = mommy.make('tasking.Task', name='Cow Price')
        mocked_target_object = mommy.make('tasking.Task')
        now = timezone.now()

        data = {
            'name': 'Milk Production',
            'description': 'Some description',
            'start': now,
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.task_type.id,
            'target_id': mocked_target_object.id,
            'parent': mocked_parent_task.id
        }

        serializer_instance = TaskSerializer(data=data)

        self.assertTrue(serializer_instance.is_valid())

        task = serializer_instance.save()

        self.assertEqual(mocked_parent_task, task.parent)
