# -*- coding: utf-8 -*-
"""
Test for Occurrence model
"""
from __future__ import unicode_literals

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
        item = mommy.make(
            'tasking.TaskOccurrence',
            date=datetime.date(2018, 5, 24),
            start_time=datetime.time(7, 0, tzinfo=pytz.utc),
            end_time=datetime.time(14, 30, tzinfo=pytz.utc)
        )
        expected = '{} - 24th May 2018, 7 a.m. to 2:30 p.m.'.format(item.task)
        self.assertEqual(expected, item.__str__())

    def test_task_occurrence_timestring(self):
        """
        Test that we get the right timestring
        """
        item = mommy.make(
            'tasking.TaskOccurrence',
            date=datetime.date(2018, 5, 22),
            start_time=datetime.time(7, 0, tzinfo=pytz.utc),
            end_time=datetime.time(14, 30, tzinfo=pytz.utc)
        )
        expected = '22nd May 2018, 7 a.m. to 2:30 p.m.'
        self.assertEqual(expected, item.get_timestring())
