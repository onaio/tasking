"""
Test for Occurrence model
"""
import datetime

from django.test import TestCase

import pytz
from model_mommy import mommy


class TestOccurrence(TestCase):
    """
    Test class for TaskOccurence models
    """

    def test_task_occurrence_model_str(self):
        """
        Test __str__ method of TaskOccurrence model
        """
        # without location
        item = mommy.make(
            "tasking.TaskOccurrence",
            date=datetime.date(2018, 5, 24),
            start_time=datetime.time(7, 0, tzinfo=pytz.utc),
            end_time=datetime.time(14, 30, tzinfo=pytz.utc),
        )
        expected = f"{item.task.name} - 24th May 2018, 7 a.m. to 2:30 p.m."
        self.assertEqual(expected, item.__str__())

        # with location
        item = mommy.make(
            "tasking.TaskOccurrence",
            location=mommy.make("tasking.Location"),
            date=datetime.date(2018, 5, 24),
            start_time=datetime.time(7, 0, tzinfo=pytz.utc),
            end_time=datetime.time(14, 30, tzinfo=pytz.utc),
        )
        expected = (
            f"{item.task.name} at {item.location.name}"
            " - 24th May 2018, 7 a.m. to 2:30 p.m."
        )
        self.assertEqual(expected, item.__str__())

    def test_task_occurrence_timestring(self):
        """
        Test that we get the right timestring
        """
        item = mommy.make(
            "tasking.TaskOccurrence",
            date=datetime.date(2018, 5, 22),
            start_time=datetime.time(7, 0, tzinfo=pytz.utc),
            end_time=datetime.time(14, 30, tzinfo=pytz.utc),
        )
        expected = "22nd May 2018, 7 a.m. to 2:30 p.m."
        self.assertEqual(expected, item.get_timestring())
