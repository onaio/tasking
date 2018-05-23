# -*- coding: utf-8 -*-
"""
Tests for tasking utils
"""
from __future__ import unicode_literals

from datetime import timedelta

import os
import zipfile

from django.test import TestCase
from django.utils import timezone

import pytz
from dateutil.parser import parse
from dateutil.rrule import rrulestr

from tasking.exceptions import TargetDoesNotExist, ShapeFileNotFound
from tasking.exceptions import MissingFiles, UnnecessaryFiles
from tasking.models import Task

from tasking.utils import (get_rrule_end, get_rrule_start, get_target,
                           validate_rrule, get_shapefile)

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

    def test_validate_rrule(self):
        """
        Test validate_rrule
        """
        # test that a valid rrule works
        self.assertTrue(validate_rrule("RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5"))
        # test that invalid rrules return False
        self.assertFalse(validate_rrule(1337))
        self.assertFalse(validate_rrule({}))
        self.assertFalse(validate_rrule([]))
        self.assertFalse(validate_rrule((12, 23)))
        self.assertFalse(validate_rrule("SELECT * FROM auth_user;"))
        self.assertFalse(validate_rrule("random string"))

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
