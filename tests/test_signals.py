# -*- coding: utf-8 -*-
"""
Tests for tasking signals
"""
from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from tasking.models import TaskOccurrence


class TestSignals(TestCase):
    """
    Test class for tasking signals
    """

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
