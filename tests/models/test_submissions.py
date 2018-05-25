# -*- coding: utf-8 -*-
"""
Test for Submission model
"""
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import six

from model_mommy import mommy


class TestSubmission(TestCase):
    """
    Test for Submission Model
    """

    def test_submission_model_str(self):
        """
        Test the string representation of Submission Model
        """
        cattle = mommy.make(
            'tasking.Task',
            name='Cattle Price')
        submission = mommy.make(
            'tasking.Submission',
            task=cattle,
            _fill_optional=['user', 'comment', 'submission_time'])
        expected = "Cattle Price - {} submission {}".format(
            submission.task.id, submission.id)
        self.assertEqual(expected, six.text_type(submission))
