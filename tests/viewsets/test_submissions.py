# -*- coding: utf-8 -*-
"""
Tests Submission viewsets.
"""
from __future__ import unicode_literals

from django.utils import six, timezone

from datetime import timedelta
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.base import TestBase

from tasking.common_tags import TARGET_DOES_NOT_EXIST, CANT_EDIT_TASK
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

    # pylint: disable=too-many-locals
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
        # pylint: disable=no-member
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
        user3 = mommy.make('auth.User')
        task = mommy.make('tasking.Task')
        submission_data = self._create_submission()
        submission_data2 = self._create_submission()
        submission_data3 = self._create_submission()

        data = {
            'target_content_type': self.user_type.id,
            'target_id': user.id,
            }
        # test that target_content_type and target_id can be changed
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

        data3 = {
            'task': task.id
        }
        # test an error is raised when trying to change task
        view3 = SubmissionViewSet.as_view({'patch': 'partial_update'})
        request3 = self.factory.patch(
            '/submission/{id}'.format(id=submission_data3['id']), data=data3)
        force_authenticate(request3, user=user3)
        response3 = view3(request=request3, pk=submission_data3['id'])

        self.assertEqual(response3.status_code, 400)
        self.assertIn('task', response3.data.keys())
        self.assertEqual(CANT_EDIT_TASK,
                         six.text_type(response3.data['task'][0]))

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
        request2 = self.factory.get(
            '/submissions/{id}'.format(id=submission.id))
        response2 = view2(request=request2, pk=submission.id)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response2.data['detail']))

        # test that you need authentication for listing submissions
        view3 = SubmissionViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/submissions')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response3.data['detail']))

        # test that you need authentication for deleting a submission
        # pylint: disable=no-member
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

        # test that you need authentication for updating a submission
        data = {
            'approved': False,
            }

        view5 = SubmissionViewSet.as_view({'patch': 'partial_update'})
        request5 = self.factory.patch(
            '/submissions/{id}'.format(id=submission.id), data=data)
        response5 = view5(request=request5, pk=submission.id)

        self.assertEqual(response5.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response5.data['detail']))

    def test_search(self):
        """
        Test that you can search for submissions.
        """
        user = mommy.make('auth.User')

        task1 = mommy.make('tasking.Task')
        task2 = mommy.make('tasking.Task', name='Hyperion')

        sub1 = mommy.make('tasking.Submission', task=task2)
        mommy.make('tasking.Submission', task=task1)

        # there are two submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 2)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # Test that we can search by task_name and get back what we expect
        request = self.factory.get('/submissions', {'search': 'Hyperion'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], sub1.id)
        self.assertEqual(len(response.data), 1)

        # test that we get no results for a name that doesn't exist
        request = self.factory.get('/submissions', {'search': 'invalid'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_task_filter(self):
        """
        Test that you can filter by task
        """
        user = mommy.make('auth.User')
        task = mommy.make('tasking.Task')

        # make a bunch of submissions
        mommy.make('tasking.Submission', _quantity=7)

        # make one submission using the task
        submission = mommy.make('tasking.Submission', task=task)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test that we get submissions for our task
        request = self.factory.get('/submissions', {'task': task.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

    def test_location_filter(self):
        """
        Test that you can filter by location
        """
        user = mommy.make('auth.User')
        location = mommy.make('tasking.Location')

        # make a bunch of submissions
        mommy.make('tasking.Submission', _quantity=7)

        # make one submission using the location
        submission = mommy.make('tasking.Submission', location=location)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test that we get submissions for our location
        request = self.factory.get('/submissions', {'location': location.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

    def test_user_filter(self):
        """
        Test that you can filter by user
        """
        user = mommy.make('auth.User')
        mosh = mommy.make('auth.User', username='mosh')

        # make a bunch of submissions
        mommy.make('tasking.Submission', _quantity=7)

        # make one submission using the user mosh
        submission = mommy.make('tasking.Submission', user=mosh)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test that we get submissions for our user mosh
        request = self.factory.get('/submissions', {'user': mosh.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

    def test_approved_filter(self):
        """
        Test that you can filter by approved
        """
        user = mommy.make('auth.User')

        # make a bunch of submissions
        mommy.make('tasking.Submission', approved=False, _quantity=7)

        # make one submission where approved is True
        submission = mommy.make('tasking.Submission', approved=True)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test that we get approved submissions
        request = self.factory.get('/submissions', {'approved': 1})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

        # test that we get not approved submissions
        request = self.factory.get('/submissions', {'approved': 0})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

    def test_valid_filter(self):
        """
        Test that you can filter by valid
        """
        user = mommy.make('auth.User')

        # make a bunch of submissions
        mommy.make('tasking.Submission', valid=False, _quantity=7)

        # make one submission where valid is True
        submission = mommy.make('tasking.Submission', valid=True)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test that we get valid submissions
        request = self.factory.get('/submissions', {'valid': 1})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], submission.id)

        # test that we get not valid submissions
        request = self.factory.get('/submissions', {'valid': 0})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

    def test_submission_time_sorting(self):
        """
        Test that you can sort by submission_time
        """
        now = timezone.now()
        user = mommy.make('auth.User')
        # make some submissions
        for i in range(0, 7):
            mommy.make('tasking.Submission', submission_time=now -
                       timedelta(days=i))

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test sorting
        request = self.factory.get(
            '/submissions', {'ordering': '-submission_time'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        # we have the expected number of records
        self.assertEqual(len(response.data), 7)
        # the first record is what we expect
        # pylint: disable=no-member
        self.assertEqual(
            response.data[0]['id'],
            Submission.objects.order_by('-submission_time').first().id)
        self.assertEqual(
            response.data[0]['submission_time'],
            Submission.objects.order_by(
                '-submission_time').first().submission_time.isoformat())
        # the last record is what we epxect
        self.assertEqual(
            response.data[-1]['id'],
            Submission.objects.order_by('-submission_time').last().id)
        self.assertEqual(
            response.data[-1]['submission_time'],
            Submission.objects.order_by(
                '-submission_time').last().submission_time.isoformat())

    def test_valid_sorting(self):
        """
        Test that you can sort by valid
        """
        user = mommy.make('auth.User')

        # make a bunch of submissions
        mommy.make('tasking.Submission', valid=False, _quantity=7)

        # make one submission where valid is True
        submission = mommy.make('tasking.Submission', valid=True)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test sorting by valid
        request = self.factory.get('/submissions', {'ordering': 'valid'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(
            response.data[0]['id'],
            Submission.objects.order_by('valid').first().id)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.data[-1]['id'], submission.id)

    def test_approved_sorting(self):
        """
        Test that you can sort by approved
        """
        user = mommy.make('auth.User')

        # make a bunch of submissions
        mommy.make('tasking.Submission', approved=True, _quantity=7)

        # make one submission where approved is False
        submission = mommy.make('tasking.Submission', approved=False)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 8)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test sorting by approved
        request = self.factory.get('/submissions', {'ordering': '-approved'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(
            response.data[0]['id'],
            Submission.objects.order_by('-approved').first().id)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.data[-1]['id'], submission.id)

    def test_created_sorting(self):
        """
        Test sorting by created
        """
        user = mommy.make('auth.User')

        # create a bunch of submissions
        mommy.make('tasking.Submission', _quantity=100)

        # check that we have 8 submissions
        # pylint: disable=no-member
        self.assertEqual(Submission.objects.all().count(), 100)

        view = SubmissionViewSet.as_view({'get': 'list'})

        # test sorting by created
        request = self.factory.get('/submissions', {'ordering': '-created'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 100)
        self.assertEqual(
            response.data[0]['id'],
            Submission.objects.order_by('-created').first().id)
        self.assertEqual(
            response.data[0]['created'],
            Submission.objects.order_by(
                '-created').first().created.isoformat())
        self.assertEqual(
            response.data[-1]['id'],
            Submission.objects.order_by('-created').last().id)
        self.assertEqual(
            response.data[-1]['created'],
            Submission.objects.order_by(
                '-created').last().created.isoformat())
