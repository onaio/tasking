# -*- coding: utf-8 -*-
"""
Tests Submission viewsets.
"""
from __future__ import unicode_literals

from django.utils import six, timezone

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.base import TestBase

from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.models import Submission
from tasking.viewsets import SubmissionViewSet


class TestSubmissionViewSet(TestBase):
    """
    Test SubmissionViewSet class.
    """

    def setUp(self):
        super(TestSubmissionViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_submission(self):
        """
        Helper to create a single submission
        """
        now = timezone.now()
        mocked_target_object = mommy.make('auth.User')
        mocked_task = mommy.make('tasking.Task', name='Cow Prices')
        mocked_location = mommy.make('tasking.Location', name='Nairobi')
        mocked_user = mommy.make('auth.User')

        data = {
            'task': mocked_task.id,
            'location': mocked_location.id,
            'submission_time': now,
            'user': mocked_user.id,
            'comments': 'Approved',
            'approved': True,
            'valid': True,
            'target_content_type': self.user_type.id,
            'target_id': mocked_target_object.id,
        }

        view = SubmissionViewSet.as_view({'post': 'create'})
        request = self.factory.post('/submissions', data)
        # Need authenticated user
        force_authenticate(request, user=mocked_user)
        response = view(request=request)
        # Convert start to an isoformat
        data['submission_time'] = now.isoformat()

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(mocked_task.id, response.data['task'])
        self.assertEqual(mocked_location.id, response.data['location'])
        self.assertEqual(mocked_user.id, response.data['user'])
        self.assertDictContainsSubset(data, response.data)

        return response.data

    def test_create_submission(self):
        """
        Test POST /submissions adding a new submission.
        """
        self._create_submission()

    def test_create_with_bad_data(self):
        """
        Test that we get appropriate errors when trying to create an object
        with bad data
        """
        bob_user = mommy.make('auth.User')
        alice_user = mommy.make('auth.User')
        now = timezone.now()
        mocked_target_object = mommy.make('auth.User')
        mocked_task = mommy.make('tasking.Task', name='Cow Prices')
        mocked_location = mommy.make('tasking.Location', name='Nairobi')
        mocked_user = mommy.make('auth.User', username='Bob')

        bad_target_id = dict(
            task=mocked_task.id,
            location=mocked_location.id,
            submission_time=now,
            user=mocked_user.id,
            comments='Approved',
            approved=True,
            valid=True,
            target_content_type=self.user_type.id,
            target_id=5487,
        )

        view1 = SubmissionViewSet.as_view({'post': 'create'})
        request1 = self.factory.post('/submissions', bad_target_id)
        # Need authenticated user
        force_authenticate(request1, user=bob_user)
        response1 = view1(request=request1)

        self.assertEqual(response1.status_code, 400)

        self.assertIn('target_id', response1.data.keys())
        self.assertEqual(TARGET_DOES_NOT_EXIST,
                         six.text_type(response1.data['target_id'][0]))

        bad_content_type = dict(
            task=mocked_task.id,
            location=mocked_location.id,
            submission_time=now,
            user=mocked_user.id,
            comments='Approved',
            approved=True,
            valid=True,
            target_content_type=999,
            target_id=mocked_target_object.id,
        )

        view2 = SubmissionViewSet.as_view({'post': 'create'})
        request2 = self.factory.post('/submissions', bad_content_type)
        # Need authenticated user
        force_authenticate(request2, user=alice_user)
        response2 = view2(request=request2)

        self.assertEqual(response2.status_code, 400)

        self.assertIn('target_content_type', response2.data.keys())
        self.assertEqual(
            'Invalid pk "999" - object does not exist.',
            six.text_type(response2.data['target_content_type'][0]))

    def test_delete_submissions(self):
        """
        Test DELETE submissions.
        """
        user = mommy.make('auth.User')
        submission = mommy.make('tasking.Submission')

        # assert that submission exists
        self.assertTrue(Submission.objects.filter(pk=submission.id).exists())
        # delete submission
        view = SubmissionViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(
            '/submissions/{id}'.format(id=submission.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=submission.id)
        # assert that submission was deleted
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Submission.objects.filter(pk=submission.id).exists())

    def test_retrieve_submission(self):
        """
        Test GET /submissions/[pk] return a submission matching pk.
        """
        user = mommy.make('auth.User')
        submission_data = self._create_submission()
        view = SubmissionViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/submission/{id}'.format(id=submission_data['id']))

        force_authenticate(request, user=user)

        response = view(request=request, pk=submission_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, submission_data)

    def test_list_submissions(self):
        """
        Test GET /submissions listing of submissions.
        """
        user = mommy.make('auth.User')
        submission_data = self._create_submission()
        view = SubmissionViewSet.as_view({'get': 'list'})

        request = self.factory.get('/submissions')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data.pop(), submission_data)

    def test_update_submission(self):
        """
        Test UPDATE submission
        """
        user = mommy.make('auth.User')
        user2 = mommy.make('auth.User')
        submission_data = self._create_submission()
        submission_data2 = self._create_submission()

        data = {
            'target_content_type': self.user_type.id,
            'target_id': user.id,
            }

        view = SubmissionViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/submission/{id}'.format(id=submission_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=submission_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.user_type.id,
            response.data['target_content_type'])
        self.assertEqual(user.id, response.data['target_id'])

        data2 = {
            'valid': True,
            'comments': 'Hello there!',
            }

        view2 = SubmissionViewSet.as_view({'patch': 'partial_update'})
        request2 = self.factory.patch(
            '/submission/{id}'.format(id=submission_data2['id']), data=data2)
        force_authenticate(request2, user=user2)
        response2 = view2(request=request2, pk=submission_data2['id'])

        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.data['valid'])
        self.assertEqual(
            'Hello there!',
            response2.data['comments'])

        def test_authentication_required(self):
            """
            Test that authentication is required for all viewset actions
            """
            now = timezone.now()
            mocked_target_object = mommy.make('auth.User')
            mocked_task = mommy.make('tasking.Task', name='Cow Prices')
            mocked_location = mommy.make('tasking.Location', name='Nairobi')
            mocked_user = mommy.make('auth.User')
            submission = mommy.make('tasking.Submission')
            submission_data = self._create_submission()

            data = {
                'task': mocked_task.id,
                'location': mocked_location.id,
                'submission_time': now,
                'user': mocked_user.id,
                'comments': 'Approved',
                'approved': True,
                'valid': True,
                'target_content_type': self.user_type.id,
                'target_id': mocked_target_object.id,
            }

            # test that you need authentication for creating a submission
            view = SubmissionViewSet.as_view({'post': 'create'})
            request = self.factory.post('/submissions', data)
            response = view(request=request)

            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                'Authentication credentials were not provided.',
                six.text_type(response.data['detail']))

            # test that you need authentication for retrieving a submission
            view2 = SubmissionViewSet.as_view({'get': 'retrieve'})
            request2 = self.factory.get('/task/{id}'.format(id=data['id']))
            response2 = view2(request=request2, pk=data['id'])
            self.assertEqual(response2.status_code, 403)
            self.assertEqual(
                'Authentication credentials were not provided.',
                six.text_type(response2.data['detail']))

            # test that you need authentication for listing a task
            view3 = SubmissionViewSet.as_view({'get': 'list'})
            request3 = self.factory.get('/tasks')
            response3 = view3(request=request3)
            self.assertEqual(response3.status_code, 403)
            self.assertEqual(
                'Authentication credentials were not provided.',
                six.text_type(response3.data['detail']))

            # test that you need authentication for deleting a task
            self.assertTrue(
                Submission.objects.filter(pk=submission.id).exists())

            view4 = SubmissionViewSet.as_view({'delete': 'destroy'})
            request4 = self.factory.delete(
                '/tasks/{id}'.format(id=submission.id))
            response4 = view4(request=request4, pk=submission.id)

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

            view5 = SubmissionViewSet.as_view({'patch': 'partial_update'})
            request5 = self.factory.patch(
                '/task/{id}'.format(id=data['id']), data=data)
            response5 = view5(request=request5, pk=submission_data['id'])

            self.assertEqual(response5.status_code, 403)
            self.assertEqual(
                'Authentication credentials were not provided.',
                six.text_type(response5.data['detail']))
