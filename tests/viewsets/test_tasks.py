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

    # pylint: disable=too-many-locals
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
            'target_content_type': self.user_type.id,
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

    def test_location_filter(self):
        """
        Test that you can filter by location
        """
        user = mommy.make('auth.User')
        nairobi = mommy.make('tasking.Location', name='Nairobi')
        arusha = mommy.make('tasking.Location', name='Arusha')
        for i in range(0, 7):
            task = mommy.make('tasking.Task')
            task.locations.add(nairobi)

        view = TaskViewSet.as_view({'get': 'list'})

        # assert that there are no tasks for Arusha
        request = self.factory.get('/tasks', {'locations': arusha.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(Task.objects.filter(locations=arusha).count(), 0)

        # assert that there are 7 tasks for Nairobi
        request = self.factory.get('/tasks', {'locations': nairobi.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(Task.objects.filter(locations=nairobi).count(), 7)

        # add one Arusha task and assert that we get it back
        task2 = mommy.make('tasking.Task')
        task2.locations.add(arusha)
        request = self.factory.get('/tasks', {'locations': arusha.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Task.objects.filter(locations=arusha).count(), 1)

    def test_parent_filter(self):
        """
        Test that you can filter by parent
        """
        user = mommy.make('auth.User')
        parent1 = mommy.make('tasking.Task')
        parent2 = mommy.make('tasking.Task')

        mommy.make('tasking.Task', parent=parent1, _quantity=7)

        view = TaskViewSet.as_view({'get': 'list'})

        # assert that there are no tasks whose parent is parent2
        request = self.factory.get('/tasks', {'parent': parent2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(Task.objects.filter(parent=parent2.id).count(), 0)

        # assert that there are 7 tasks whose parent is parent1
        request = self.factory.get('/tasks', {'parent': parent1.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(Task.objects.filter(parent=parent1.id).count(), 7)

        # create a task whose parent is parent2 and assert its there
        mommy.make('tasking.Task', parent=parent2)

        request = self.factory.get('/tasks', {'parent': parent2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Task.objects.filter(parent=parent2.id).count(), 1)

    def test_status_filter(self):
        """
        Test that you can filter by status
        """
        user = mommy.make('auth.User')
        mommy.make('tasking.Task', status=Task.DEACTIVATED, _quantity=7)

        view = TaskViewSet.as_view({'get': 'list'})

        # assert that there are no tasks with an Active Status
        request = self.factory.get('/tasks', {'status': Task.ACTIVE})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(Task.objects.filter(status=Task.ACTIVE).count(), 0)

        # assert that there are 7 tasks with an Deactivated Status
        request = self.factory.get('/tasks', {'status': Task.DEACTIVATED})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(
            Task.objects.filter(status=Task.DEACTIVATED).count(), 7)

        # add a task with with an Active Status and assert that we get it back
        mommy.make('tasking.Task', status=Task.ACTIVE)
        request = self.factory.get('/tasks', {'status': Task.ACTIVE})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Task.objects.filter(status=Task.ACTIVE).count(), 1)

    def test_project_filter(self):
        """
        Test that you can filter by Project
        """
        user = mommy.make('auth.User')
        project1 = mommy.make('tasking.Project', name='Test Case Scenario')
        project2 = mommy.make('tasking.Project', name='Reality Check')
        for i in range(0, 7):
            task = mommy.make('tasking.Task')
            project1.tasks.add(task)

        view = TaskViewSet.as_view({'get': 'list'})
        # assert that there are no tasks in project Reality Check
        request = self.factory.get('/tasks', {'project': project2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(
            Task.objects.filter(project=project2.id).count(), 0)

        # assert that there are 7 tasks in project Test Case Scenario
        request = self.factory.get('/tasks', {'project': project1.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(
            Task.objects.filter(project=project1.id).count(), 7)

        # add a task to project Reality Check and assert its there
        task2 = mommy.make('tasking.Task')
        project2.tasks.add(task2)

        request = self.factory.get('/tasks', {'project': project2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            Task.objects.filter(project=project2.id).count(), 1)

    def test_name_search(self):
        """
        Test that you can search by Name
        """
        user = mommy.make('auth.User')
        mommy.make('tasking.Task', name='Cattle Price')
        mommy.make('tasking.Task', name='Chicken Price', _quantity=7)

        view = TaskViewSet.as_view({'get': 'list'})
        request = self.factory.get('/tasks', {'search': 'Cattle Price'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            Task.objects.filter(name='Cattle Price').count(), 1)

    def test_task_sorting(self):
        """
        Test that sorting works
        """
        user = mommy.make('auth.User')
        project1 = mommy.make('tasking.Project')
        project2 = mommy.make('tasking.Project')
        task1 = mommy.make(
            'tasking.Task', name='Milk Production Size', status=Task.DRAFT)
        for i in range(0, 7):
            # create other tasks
            task = mommy.make(
                'tasking.Task', name='Cow Price', status=Task.DEACTIVATED)
            project1.tasks.add(task)
        task2 = mommy.make(
            'tasking.Task',
            name='Allocated land for farming', status=Task.ACTIVE)
        project2.tasks.add(task2)
        view = TaskViewSet.as_view({'get': 'list'})

        # order by status descending
        request = self.factory.get('/tasks', {'ordering': '-status'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.data[0]['id'], task1.id)
        self.assertEqual(response.data[0]['status'], task1.status)
        self.assertEqual(response.data[-1]['id'], task2.id)
        self.assertEqual(response.data[-1]['status'], task2.status)

        # order by created ascending
        request = self.factory.get('/tasks', {'ordering': 'created'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data[0]['created'], task1.created.isoformat())
        self.assertEqual(response.data[0]['id'], task1.id)
        self.assertEqual(
            response.data[-1]['created'], task2.created.isoformat())
        self.assertEqual(response.data[-1]['id'], task2.id)

        # order by name ascending
        request = self.factory.get('/tasks', {'ordering': 'name'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(
            response.data[-1]['name'], task1.name)
        self.assertEqual(response.data[-1]['id'], task1.id)
        self.assertEqual(
            response.data[0]['name'], task2.name)
        self.assertEqual(response.data[0]['id'], task2.id)

        # order by project ascending
        request = self.factory.get('/tasks', {'project': project2.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], task2.name)
        self.assertEqual(
            Task.objects.filter(project=project2.id).count(), 1)

    def test_search_filter_order(self):
        """
        Test that you can search filter and order at the same time
        """
        user = mommy.make('auth.User')

        task = mommy.make(
            'tasking.Task', name='Cattle Price', status=Task.ACTIVE)
        task2 = mommy.make(
            'tasking.Task', name='Cattle Price', status=Task.ACTIVE)

        mommy.make('tasking.Task', name='Cattle Price', status=Task.DRAFT)

        for i in range(0, 4):
            mommy.make(
                'tasking.Task', name='Cattle Price', status=Task.DEACTIVATED)

        view = TaskViewSet.as_view({'get': 'list'})

        request = self.factory.get(
            '/tasks?search={name}&status={status}&ordering={order}'.format(
                name='Cattle Price', status=Task.ACTIVE, order='created'))
        force_authenticate(request, user=user)

        response = view(request=request)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['status'], task.status)
        self.assertEqual(response.data[0]['id'], task.id)
        self.assertEqual(response.data[1]['status'], task2.status)
        self.assertEqual(response.data[1]['id'], task2.id)
