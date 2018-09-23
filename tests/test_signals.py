"""
Tests for tasking signals
"""
from django.db.models.signals import post_save
from django.test import TestCase

from model_mommy import mommy

from tasking.models import TaskOccurrence
from tasking.signals import create_occurrences


class TestSignals(TestCase):
    """
    Test class for tasking signals
    """

    def setUp(self):
        """
        Setup the Signal tests
        """
        post_save.connect(create_occurrences, sender='tasking.Task',
                          dispatch_uid='create_task_occurrences')

    def test_task_occurrences(self):
        """
        Test that task occurrences are created when a new Task object is
        created
        """

        # create a Task object
        task = mommy.make(
            'tasking.Task',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=57'
        )
        # pylint: disable=no-member
        self.assertEqual(57, TaskOccurrence.objects.filter(task=task).count())
