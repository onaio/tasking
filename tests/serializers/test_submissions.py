"""
Test for SubmissionSerializer
"""
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytz
from model_mommy import mommy
from tests.base import TestBase

from tasking.models import Submission
from tasking.serializers import SubmissionSerializer

USER = get_user_model()


class TestSubmissionSerializer(TestBase):
    """
    Tests for SubmissionSerializer
    """

    def test_create_submission(self):
        """
        Test that the serializer creates a submission
        """
        now = timezone.now()
        mocked_target_object = mommy.make('auth.User')
        mocked_task = mommy.make('tasking.Task', name='Cow Prices')
        mocked_location = mommy.make('tasking.Location', name='Nairobi')
        mocked_user = mommy.make('auth.User', username='Bob')

        data = {
            'task': mocked_task.id,
            'location': mocked_location.id,
            'submission_time': now,
            'user': mocked_user.id,
            'comments': 'Approved',
            'status': Submission.REJECTED,
            'valid': True,
            'target_content_type': self.user_type.id,
            'target_id': mocked_target_object.id,
        }

        serializer_instance = SubmissionSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())

        submission = serializer_instance.save()

        # the subsmission_time field is going to be converted to isformat
        data['submission_time'] = now.astimezone(
            pytz.timezone('Africa/Nairobi')).isoformat()
        self.assertDictContainsSubset(data, serializer_instance.data)

        self.assertEqual(mocked_task, submission.task)
        self.assertEqual(mocked_location, submission.location)
        self.assertEqual(mocked_user, submission.user)
        self.assertEqual(now, submission.submission_time)
        self.assertEqual('Approved', submission.comments)
        self.assertEqual(Submission.REJECTED, submission.status)
        self.assertTrue(submission.valid)

        # assert Submission approved property is False when status is REJECTED
        self.assertFalse(submission.approved)

        # set Submission status to APPROVED and test that approved is True
        submission.status = Submission.APPROVED
        self.assertTrue(submission.approved)

        expected_fields = {
            'task',
            'location',
            'submission_time',
            'user',
            'comments',
            'status',
            'valid',
            'target_content_type',
            'target_id',
            'id',
            'created',
            'modified'
        }

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))

    def test_validate_bad_data(self):
        """
        Test validate method of SubmissionSerializer works as expected
        for bad data
        """
        now = timezone.now()
        mocked_target_object = mommy.make('auth.User')
        mocked_task = mommy.make('tasking.Task', name='Cow Prices')
        mocked_location = mommy.make('tasking.Location', name='Nairobi')
        mocked_user = mommy.make('auth.User', username='Bob')

        bad_target_id = OrderedDict(
            task=mocked_task.id,
            location=mocked_location.id,
            submission_time=now,
            user=mocked_user.id,
            comments='Approved',
            status=Submission.APPROVED,
            valid=True,
            target_content_type=self.user_type.id,
            target_id=5487,
        )

        self.assertFalse(SubmissionSerializer(data=bad_target_id).is_valid())

        bad_content_type = OrderedDict(
            task=mocked_task.id,
            location=mocked_location.id,
            submission_time=now,
            user=mocked_user.id,
            comments='Approved',
            status=Submission.APPROVED,
            valid=True,
            target_content_type='foobar',
            target_id=mocked_target_object.id,
        )

        self.assertFalse(
            SubmissionSerializer(data=bad_content_type).is_valid())
