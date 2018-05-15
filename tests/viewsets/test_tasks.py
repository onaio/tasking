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
        Test POST /task adding a new task.
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

    def test_update_task(self):
        """
        Test UPDATE task
        """
        user = mommy.make('auth.User')
        user2 = mommy.make('auth.User')
        task_data = self._create_task()
        task_data2 = self._create_task()

        data = {
            'name': "Milk Price",
            'target_content_type': self.user_type.id,
            'target_id': user.id,
            }

        view = TaskViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/task/{id}'.format(id=task_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=task_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual('Milk Price', response.data['name'])
        self.assertEqual(
            self.user_type.id,
            response.data['target_content_type'])
        self.assertEqual(user.id, response.data['target_id'])

        data2 = {
            'name': "Cattle Price",
            'description': 'Hello there!',
            }

        view2 = TaskViewSet.as_view({'patch': 'partial_update'})
        request2 = self.factory.patch(
            '/task/{id}'.format(id=task_data2['id']), data=data2)
        force_authenticate(request2, user=user2)
        response2 = view2(request=request2, pk=task_data2['id'])

        self.assertEqual(response2.status_code, 200)
        self.assertEqual('Cattle Price', response2.data['name'])
        self.assertEqual(
            'Hello there!',
            response2.data['description'])

    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        mocked_target_object = mommy.make('tasking.Task')
        task_data = self._create_task()
        task = mommy.make('tasking.Task')
        user = mommy.make('auth.User')

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
        view = TaskViewSet.as_view({'post': 'create'})
        request = self.factory.post('/tasks', good_data)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response.data['detail']))

        # test that you need authentication for retrieving a task
        view2 = TaskViewSet.as_view({'get': 'retrieve'})
        request2 = self.factory.get('/task/{id}'.format(id=task_data['id']))
        response2 = view2(request=request2, pk=task_data['id'])
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response2.data['detail']))

        # test that you need authentication for listing a task
        view3 = TaskViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/tasks')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response3.data['detail']))

        # test that you need authentication for deleting a task
        self.assertTrue(Task.objects.filter(pk=task.id).exists())

        view4 = TaskViewSet.as_view({'delete': 'destroy'})
        request4 = self.factory.delete('/tasks/{id}'.format(id=task.id))
        response4 = view4(request=request4, pk=task.id)

        self.assertEqual(response4.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response4.data['detail']))

        # test that you need authentication for updating a task
        data = {
            'name': "Milk Price",
            'target_content_type': self.task_type.id,
            'target_id': user.id,
            }

        view5 = TaskViewSet.as_view({'patch': 'partial_update'})
        request5 = self.factory.patch(
            '/task/{id}'.format(id=task_data['id']), data=data)
        response5 = view5(request=request5, pk=task_data['id'])

        self.assertEqual(response5.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response5.data['detail']))
