# -*- coding: utf-8 -*-
"""
Tests for tasking utils
"""
from __future__ import unicode_literals

import os
import zipfile
from datetime import datetime, time, timedelta

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone

import pytz
from dateutil.parser import parse
from dateutil.rrule import rrulestr
from model_mommy import mommy

from tasking.exceptions import (MissingFiles, ShapeFileNotFound,
                                TargetDoesNotExist, UnnecessaryFiles)
from tasking.models import Task, TaskOccurrence
from tasking.utils import (MAX_OCCURRENCES, generate_task_occurrences,
                           generate_tasklocation_occurrences,
                           get_allowed_contenttypes, get_occurrence_end_time,
                           get_occurrence_start_time, get_rrule_end,
                           get_rrule_start, get_shapefile, get_target)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestUtils(TestCase):
    """
    Test class for tasking utils
    """

    def test_get_target(self):
        """
        Test get_target
        """
        # check that we can get a content type corectly
        task_contenttype = get_target(app_label='tasking', target_type='task')
        self.assertEqual(task_contenttype.model_class(), Task)
        # check that we get TargetDoesNotExist when the content type does
        # not exist
        with self.assertRaises(TargetDoesNotExist):
            get_target(app_label='foo', target_type='bar')

    def test_get_rrule_start(self):
        """
        Test that get_rrule_start returns the rrule start correctly
        """
        # test when DTSTART is provided
        rule1 = 'DTSTART:19970902T090000 RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        start1 = get_rrule_start(rrulestr(rule1))
        # must be timezone aware
        self.assertTrue(timezone.is_aware(start1))
        # check that it matches the datetime
        expected1 = timezone.make_aware(parse("19970902T090000"))
        self.assertEqual(expected1, start1)

        # test when DTSTART is not provided
        rule2 = 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        start2 = get_rrule_start(rrulestr(rule2))
        # must be timezone aware
        self.assertTrue(timezone.is_aware(start2))
        # check that it matches today
        now = timezone.now().astimezone(pytz.timezone('Africa/Nairobi'))
        self.assertEqual(now.year, start2.year)
        self.assertEqual(now.month, start2.month)
        self.assertEqual(now.day, start2.day)
        self.assertEqual(now.hour, start2.hour)

    def test_get_rrule_end(self):
        """
        Test that get_rrule_end returns the rrule end correctly
        """
        # when until is provided
        # pylint: disable=line-too-long
        rule1 = 'DTSTART:20180501T210000Z RRULE:FREQ=YEARLY;BYDAY=SU;BYSETPOS=1;BYMONTH=1;UNTIL=20480521T210000Z'  # noqa
        end1 = get_rrule_end(rrulestr(rule1))
        # must be timezone aware
        self.assertTrue(timezone.is_aware(end1))
        # must be 21 may 2018
        self.assertEqual(2048, end1.year)
        self.assertEqual(5, end1.month)
        self.assertEqual(21, end1.day)

        # when count is provided instead
        rule2 = 'RRULE:FREQ=DAILY;COUNT=5'
        end2 = get_rrule_end(rrulestr(rule2))
        # must be timezone aware
        self.assertTrue(timezone.is_aware(end2))
        # must be 4 days from now (5 occurrences with today as the first)
        now = timezone.now().astimezone(pytz.timezone('Africa/Nairobi'))
        then = now + timedelta(days=4)
        self.assertEqual(then.year, end2.year)
        self.assertEqual(then.month, end2.month)
        self.assertEqual(then.day, end2.day)

    def test_get_shapefile(self):
        """
        Test get_shapefile
        """
        path = os.path.join(
            BASE_DIR, 'tests', 'fixtures', 'test_shapefile.zip')
        zip_file = zipfile.ZipFile(path)

        path = os.path.join(
            BASE_DIR, 'tests', 'fixtures', 'test_shapefile_not_found.zip')
        zip_file1 = zipfile.ZipFile(path)

        path = os.path.join(
            BASE_DIR, 'tests', 'fixtures', 'test_missing_files.zip')
        zip_file2 = zipfile.ZipFile(path)

        path = os.path.join(
            BASE_DIR, 'tests', 'fixtures', 'test_unnecessary_files.zip')
        zip_file3 = zipfile.ZipFile(path)

        # test that we can get valid shapefile
        self.assertEqual(get_shapefile(zip_file), 'test_shapefile.shp')

        # test that we get ShapeFileNotFound when shapefile cant be located
        with self.assertRaises(ShapeFileNotFound):
            get_shapefile(zip_file1)
        # test that we get MissingFiles when zipfile is missing files
        with self.assertRaises(MissingFiles):
            get_shapefile(zip_file2)
        # test that we get UnnecessaryFiles when zipfile exceeds needed files
        with self.assertRaises(UnnecessaryFiles):
            get_shapefile(zip_file3)

    def test_get_allowed_contenttypes(self):
        """
        Test get_allowed_contenttypes
        """
        input_expected = [
            {'app_label': 'tasking', 'model': 'task'},
            {'app_label': 'tasking', 'model': 'segmentrule'}]

        task_type = ContentType.objects.get(app_label='tasking', model='task')
        rule_type = ContentType.objects.get(app_label='tasking',
                                            model='segmentrule')

        allowed = get_allowed_contenttypes(
            allowed_content_types=input_expected)

        self.assertEqual(2, allowed.count())
        self.assertIn(task_type, allowed)
        self.assertIn(rule_type, allowed)

    def test_generate_task_occurrences(self):
        """
        Test generate_task_occurrences works correctly
        """
        task1 = mommy.make(
            'tasking.Task',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        )
        task2 = mommy.make(
            'tasking.Task',
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5000'
        )

        # pylint: disable=line-too-long
        rule1 = 'DTSTART:20180501T070000Z RRULE:FREQ=YEARLY;BYDAY=SU;BYSETPOS=1;BYMONTH=1;UNTIL=20480521T210000Z'  # noqa
        task3 = mommy.make('tasking.Task', timing_rule=rule1)

        # remove any auto-generated occurrences
        # pylint: disable=no-member
        TaskOccurrence.objects.all().delete()

        # we should get 5 occurrences
        occurrences1 = generate_task_occurrences(
            task=task1, timing_rule=task1.timing_rule)
        self.assertEqual(5, occurrences1.count())

        # we should get {MAX_OCCURRENCES} occurrences
        occurrences2 = generate_task_occurrences(
            task=task2, timing_rule=task2.timing_rule)
        self.assertEqual(MAX_OCCURRENCES, occurrences2.count())

        # the start times should all be from the timing_rule, whic in this
        # case is the time the task was created
        # the end_times should all be 23:59:59
        for item in occurrences1:
            self.assertEqual(
                item.start_time.hour,
                task1.start.astimezone(
                    timezone.get_current_timezone()).time().hour)
            self.assertEqual(
                item.start_time.minute,
                task1.start.astimezone(
                    timezone.get_current_timezone()).time().minute)
            self.assertEqual(item.end_time, time(23, 59, 59, 999999))

        # we should have 30 occurrences
        occurrences3 = generate_task_occurrences(
            task=task3, timing_rule=task3.timing_rule)
        self.assertEqual(30, occurrences3.count())

        # the start times should all be from the timing_rule, whicih in this
        # case 7am
        # the end_times should all be 23:59:59 apart from the last one which
        # should be from the timing rule, which in this case is 9pm
        for item in occurrences3:
            self.assertEqual(item.start_time, time(7, 0, 0, 0))
            if item == occurrences3.last():
                self.assertEqual(item.end_time, time(21, 0, 0, 0))
            else:
                self.assertEqual(item.end_time, time(23, 59, 59, 999999))

    def test_no_same_start_and_end(self):
        """
        Test that no occurrences are created when start and end times are
        the same (because it does not make sense)
        """

        # pylint: disable=line-too-long
        rule1 = 'DTSTART:20180501T210000Z RRULE:FREQ=YEARLY;BYDAY=SU;BYSETPOS=1;BYMONTH=1;UNTIL=20280521T210000Z'  # noqa
        task = mommy.make('tasking.Task', timing_rule=rule1)

        # Delete any autogenerated occurrences
        # pylint: disable=no-member
        TaskOccurrence.objects.all().delete()

        # we should have 9 instead of 10 occurrences because the very last
        # one would start at 9pm and end at 9pm
        self.assertEqual(9, generate_task_occurrences(
            task=task, timing_rule=task.timing_rule).count())

    def test_get_occurrence_start_time(self):
        """
        Test get_occurrence_start_time
        """
        # pylint: disable=line-too-long
        rule = 'DTSTART:20180501T070000Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=500;UNTIL=20280521T210000Z'  # noqa
        the_rrule = rrulestr(rule)

        rule2 = 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        the_rrule2 = rrulestr(rule2)

        # when start_time is not input then return start_time from timing_rule
        self.assertEqual(
            "07:00:00",
            get_occurrence_start_time(
                the_rrule, start_time_input=None).isoformat())

        # if given an input, return that input
        self.assertEqual(
            "09:15:00",
            get_occurrence_start_time(
                the_rrule, start_time_input=time(9, 15, 0, 0)).isoformat())

        # when timing_rule has no explicit start then we get back is right now
        now = timezone.now().astimezone(pytz.timezone('Africa/Nairobi')).time()
        result = get_occurrence_start_time(the_rrule2, start_time_input=None)

        diff = datetime.combine(timezone.now().date(), now) -\
            datetime.combine(timezone.now().date(), result)
        # should be within one minutes of each other
        self.assertTrue(diff.seconds < 60)

    def test_get_occurrence_end_time(self):
        """
        Test get_occurrence_end_time
        """
        rule = 'RRULE:FREQ=DAILY;INTERVAL=1;COUNT=500;UNTIL=20280521T210000Z'
        the_rrule = rrulestr(rule)
        task = mommy.make('tasking.Task', timing_rule=rule)

        rule2 = 'RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5'
        the_rrule2 = rrulestr(rule2)

        # when end_time is not input then return start_time from timing_rule
        self.assertEqual(
            "21:00:00",
            get_occurrence_end_time(
                task, the_rrule, end_time_input=None).isoformat())

        # when end_time is input then return start_time from timing_rule
        self.assertEqual(
            "19:15:00",
            get_occurrence_end_time(
                task, the_rrule,
                end_time_input=time(19, 15, 0, 0)).isoformat())

        # return the end of the day when timing_rule has no end and end_
        # time is not provided
        self.assertEqual(
            "23:59:59.999999",
            get_occurrence_end_time(
                task, the_rrule2, end_time_input=None).isoformat())

    def test_generate_tasklocation_occurrences(self):
        """
        Test generate_tasklocation_occurrences
        """
        task = mommy.make('tasking.Task')
        location = mommy.make('tasking.Location')
        task_location = mommy.make(
            'tasking.TaskLocation',
            task=task,
            location=location,
            timing_rule='RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5',
            start='07:00:00',
            end='21:00:00'
        )

        # Delete any autogenerated occurrences
        # pylint: disable=no-member
        TaskOccurrence.objects.all().delete()

        occurrences = generate_tasklocation_occurrences(task_location)
        self.assertEqual(5, occurrences.count())

        # check the start and end time
        for occurrence in occurrences:
            self.assertEqual('07:00:00', occurrence.start_time.isoformat())
            self.assertEqual('21:00:00', occurrence.end_time.isoformat())