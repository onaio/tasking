# -*- coding: utf-8 -*-
"""
Tests Project viewsets.
"""
from __future__ import unicode_literals

from django.utils import six

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.base import TestBase

from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.models import Project
from tasking.viewsets import ProjectViewSet


class TestProjectViewSet(TestBase):
    """
    Test ProjectViewSet class.
    """

    def setUp(self):
        super(TestProjectViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_project(self):
        """
        Helper to create a single project
        """
        mocked_target_object = mommy.make('tasking.Task')

        task1 = mommy.make('tasking.Task')
        task2 = mommy.make('tasking.Task')

        user = mommy.make('auth.User')

        data = {
            'name': "Livestock prices",
            'target_content_type': self.task_type.id,
            'target_id': mocked_target_object.id,
        }

        data_with_projects = data.copy()
        data_with_projects['tasks'] = [task1.id, task2.id]

        view = ProjectViewSet.as_view({'post': 'create'})
        request = self.factory.post('/projects', data_with_projects)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        # we test that we do have our tasks
        self.assertEqual(set([task1.id, task2.id]),
                         set(response.data['tasks']))
        self.assertEqual(response.status_code, 201, response.data)
        # the order of tasks may have changed so a dict comparison
        # may fail, we use `data` that does not include tasks
        self.assertDictContainsSubset(data, response.data)
        return response.data

    def test_create_project(self):
        """
        Test POST /projects adding a new project.
        """
        self._create_project()

    def test_create_with_bad_data(self):
        """
        Test that we get appropriate errors when trying to create a project
        with bad data
        """
        bob_user = mommy.make('auth.User')
        alice_user = mommy.make('auth.User')
        mocked_target_object = mommy.make('tasking.Task')

        # test bad target_id validation
        bad_target_id = {
            'name': "Livestock prices",
            'target_content_type': self.task_type.id,
            'target_id': 1337,
        }

        view1 = ProjectViewSet.as_view({'post': 'create'})
        request1 = self.factory.post('/projects', bad_target_id)
        # Need authenticated user
        force_authenticate(request1, user=bob_user)
        response1 = view1(request=request1)

        self.assertEqual(response1.status_code, 400)

        self.assertIn('target_id', response1.data.keys())
        self.assertEqual(TARGET_DOES_NOT_EXIST,
                         six.text_type(response1.data['target_id'][0]))

        # test bad content type validation
        bad_content_type = {
            'name': "Half Life Three",
            'target_content_type': 999,
            'target_id': mocked_target_object.id,
        }

        view2 = ProjectViewSet.as_view({'post': 'create'})
        request2 = self.factory.post('/projects', bad_content_type)
        # Need authenticated user
        force_authenticate(request2, user=alice_user)
        response2 = view2(request=request2)

        self.assertEqual(response2.status_code, 400)

        self.assertIn('target_content_type', response2.data.keys())
        self.assertEqual(
            'Invalid pk "999" - object does not exist.',
            six.text_type(response2.data['target_content_type'][0]))

    def test_delete_project(self):
        """
        Test DELETE project.
        """
        user = mommy.make('auth.User')
        project = mommy.make('tasking.Project')

        # assert that project exists
        # pylint: disable=no-member
        self.assertTrue(Project.objects.filter(pk=project.id).exists())
        # delete project
        view = ProjectViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/projects/{id}'.format(id=project.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=project.id)
        # assert that task was deleted
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Project.objects.filter(pk=project.id).exists())

    def test_retrieve_project(self):
        """
        Test GET /projects/[pk] return a project matching pk.
        """
        user = mommy.make('auth.User')
        project_data = self._create_project()
        view = ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/project/{id}'.format(id=project_data['id']))
        force_authenticate(request, user=user)
        response = view(request=request, pk=project_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, project_data)

    def test_list_projects(self):
        """
        Test GET /projects listing of projects
        """
        user = mommy.make('auth.User')
        project_data = self._create_project()
        view = ProjectViewSet.as_view({'get': 'list'})

        request = self.factory.get('/projects')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data.pop(), project_data)

    def test_update_project(self):
        """
        Test UPDATE project
        """
        user = mommy.make('auth.User')
        user2 = mommy.make('auth.User')
        project_data = self._create_project()
        project_data2 = self._create_project()

        data = {
            'name': "project 36",
            'target_content_type': self.user_type.id,
            'target_id': user.id,
            }

        view = ProjectViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/project/{id}'.format(id=project_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=project_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual('project 36', response.data['name'])
        self.assertEqual(
            self.user_type.id,
            response.data['target_content_type'])
        self.assertEqual(user.id, response.data['target_id'])

        some_task = mommy.make('tasking.task')

        data2 = {
            'name': "Mission 99",
            'tasks': [some_task.id]
            }

        view2 = ProjectViewSet.as_view({'patch': 'partial_update'})
        request2 = self.factory.patch(
            '/project/{id}'.format(id=project_data2['id']), data=data2)
        force_authenticate(request2, user=user2)
        response2 = view2(request=request2, pk=project_data2['id'])

        self.assertEqual(response2.status_code, 200)
        self.assertEqual('Mission 99', response2.data['name'])
        self.assertEqual([some_task.id], response2.data['tasks'])

    # pylint: disable=too-many-locals
    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        mocked_target_object = mommy.make('tasking.Task')
        project_data = self._create_project()
        project = mommy.make('tasking.Project')
        user = mommy.make('auth.User')

        # test that you need authentication for creating a project
        good_data = {
            'name': "Livestock prices",
            'target_content_type': self.task_type.id,
            'target_id': mocked_target_object.id,
        }
        view = ProjectViewSet.as_view({'post': 'create'})
        request = self.factory.post('/projects', good_data)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response.data['detail']))

        # test that you need authentication for retrieving a project
        view2 = ProjectViewSet.as_view({'get': 'retrieve'})
        request2 = self.factory.get(
            '/project/{id}'.format(id=project_data['id']))
        response2 = view2(request=request2, pk=project_data['id'])
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response2.data['detail']))

        # test that you need authentication for listing projects
        view3 = ProjectViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/projects')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response3.data['detail']))

        # test that you need authentication for deleting a project
        # pylint: disable=no-member
        self.assertTrue(Project.objects.filter(pk=project.id).exists())

        view4 = ProjectViewSet.as_view({'delete': 'destroy'})
        request4 = self.factory.delete('/projects/{id}'.format(id=project.id))
        response4 = view4(request=request4, pk=project.id)

        self.assertEqual(response4.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response4.data['detail']))

        # test that you need authentication for updating a project
        data = {
            'name': "Milk Price",
            'target_content_type': self.user_type.id,
            'target_id': user.id,
            }

        view5 = ProjectViewSet.as_view({'patch': 'partial_update'})
        request5 = self.factory.patch(
            '/project/{id}'.format(id=project_data['id']), data=data)
        response5 = view5(request=request5, pk=project_data['id'])

        self.assertEqual(response5.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response5.data['detail']))
