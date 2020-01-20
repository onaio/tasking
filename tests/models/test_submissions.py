"""
Test for Submission model
"""
from django.test import TestCase

from model_mommy import mommy


class TestSubmission(TestCase):
    """
    Test for Submission Model
    """

    def test_submission_model_str(self):
        """
        Test the string representation of Submission Model
        """
        cattle = mommy.make("tasking.Task", name="Cattle Price")
        submission = mommy.make(
            "tasking.Submission",
            task=cattle,
            _fill_optional=["user", "comments", "submission_time"],
        )
        expected = f"Cattle Price - {submission.task.id}" f" submission {submission.id}"
        self.assertEqual(expected, str(submission))
