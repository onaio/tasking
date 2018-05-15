# -*- coding: utf-8 -*-
"""
Tests Task viewsets.
"""
from __future__ import unicode_literals

from django.utils import six, timezone

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.base import TestBase

from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.models import Task
from tasking.viewsets import TaskViewSet


class TestTaskViewSet(TestBase):
    """
    Test TaskViewSet class.
    """

    def setUp(self):
        super(TestTaskViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_task(self):
        """
        Helper to create a single task
        """
        now = timezone.now()
        mocked_target_object = mommy.make('tasking.Task')

        rule1 = mommy.make('tasking.SegmentRule')
        rule2 = mommy.make('tasking.SegmentRule')

        user = mommy.make('auth.User')

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

        view = TaskViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', data_with_segment_rules)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)
        # Convert start to an isoformat
        data['start'] = now.isoformat()

        # we test that we do have our segment rules
        self.assertEqual(set([rule1.id, rule2.id]),
                         set(response.data['segment_rules']))
        self.assertEqual(response.status_code, 201, response.data)
        # the order of segment_rules may have changed so a dict comparison
        # may fail, we use `data` that does not include segment rules
        self.assertDictContainsSubset(data, response.data)
        return response.data

    def test_create_task(self):
        """
        Test POST /messaging adding a new task.
        """
        self._create_task()

    def test_create_with_bad_data(self):
        """
        Test that we get appropriate errors when trying to create an object
        with bad data
        """
        bob_user = mommy.make('auth.User')
        alice_user = mommy.make('auth.User')
        mocked_target_object = mommy.make('tasking.Task')

        # test bad target_id validation
        bad_target_id = dict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type=self.task_type.id,
            target_id=1337,
        )

        view1 = TaskViewSet.as_view({'post': 'create'})
        request1 = self.factory.post('/tasks', bad_target_id)
        # Need authenticated user
        force_authenticate(request1, user=bob_user)
        response1 = view1(request=request1)

        self.assertEqual(response1.status_code, 400)
        response1.render()

        self.assertIn('target_id', response1.data.keys())
        self.assertEqual(TARGET_DOES_NOT_EXIST,
                         six.text_type(response1.data['target_id'][0]))

        # test bad content type validation
        bad_content_type = dict(
            name='Cow price',
            description='Some description',
            start=timezone.now(),
            total_submission_target=10,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            target_content_type=999,
            target_object_id=mocked_target_object.id,
        )

        view2 = TaskViewSet.as_view({'post': 'create'})
        request2 = self.factory.post('/tasks', bad_content_type)
        # Need authenticated user
        force_authenticate(request2, user=alice_user)
        response2 = view2(request=request2)

        self.assertEqual(response2.status_code, 400)

        self.assertIn('target_content_type', response2.data.keys())
        self.assertEqual(
            'Invalid pk "999" - object does not exist.',
            six.text_type(response2.data['target_content_type'][0]))

    def test_delete_task(self):
        """
        Test DELETE tasks.
        """
        user = mommy.make('auth.User')
        task = mommy.make('tasking.Task')

        # assert that task exists
        self.assertTrue(Task.objects.filter(pk=task.id).exists())
        # delete task
        view = TaskViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/tasks/{id}'.format(id=task.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=task.id)
        # assert that task was deleted
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=task.id).exists())

    def test_retrieve_task(self):
        """
        Test GET /tasks/[pk] return a task matching pk.
        """
        user = mommy.make('auth.User')
        task_data = self._create_task()
        view = TaskViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/task/{id}'.format(id=task_data['id']))
        force_authenticate(request, user=user)
        response = view(request=request, pk=task_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, task_data)

    def test_list_tasks(self):
        """
        Test GET /tasks listing of tasks for specific forms.
        """
        user = mommy.make('auth.User')
        task_data = self._create_task()
        view = TaskViewSet.as_view({'get': 'list'})

        request = self.factory.get('/tasks')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data.pop(), task_data)

    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        mocked_target_object = mommy.make('tasking.Task')

        # test that you need authentication for creating a task
        good_data = {
            'name': 'Cow price',
            'description': 'Some description',
            'start': timezone.now(),
            'total_submission_target': 10,
            'timing_rule': 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            'target_content_type': self.task_type.id,
            'target_id': mocked_target_object.id,
        }
        view3 = TaskViewSet.as_view({'post': 'create'})
        request3 = self.factory.post('/tasks', good_data)
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response3.data['detail']))

        # retrieve
        # list
        # destroy
        # update
