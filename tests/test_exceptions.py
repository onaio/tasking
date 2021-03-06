"""
Tests for tasking exceptions
"""
import os
import zipfile

from django.test import TestCase, override_settings

from tasking.common_tags import (
    MISSING_FILE,
    NO_SHAPEFILE,
    TARGET_DOES_NOT_EXIST,
    UNNECESSARY_FILE,
)
from tasking.exceptions import (
    MissingFiles,
    ShapeFileNotFound,
    TargetDoesNotExist,
    UnnecessaryFiles,
)
from tasking.utils import get_shapefile, get_target

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestExceptions(TestCase):
    """
    Test class for tasking exceptions
    """

    def test_target_does_not_exist(self):
        """
        Test TargetDoesNotExist error message is what we expect
        """
        with self.assertRaises(TargetDoesNotExist) as context:
            get_target(app_label="foo", target_type="bar")
        the_exception = context.exception
        self.assertEqual(TARGET_DOES_NOT_EXIST, the_exception.message)

    def test_shape_file_not_found(self):
        """
        Test ShapeFileNotFound error message is what we expect
        """
        path = os.path.join(BASE_DIR, "tests", "fixtures", "missing_shp.zip")
        zip_file = zipfile.ZipFile(path)

        with self.assertRaises(ShapeFileNotFound) as context:
            get_shapefile(zip_file)
        the_exception = context.exception
        self.assertEqual(NO_SHAPEFILE, the_exception.message)

    def test_missing_dbf(self):
        """
        Test missing .dbf file
        """
        path = os.path.join(BASE_DIR, "tests", "fixtures", "missing_dbf.zip")
        zip_file = zipfile.ZipFile(path)

        with self.assertRaises(MissingFiles) as context:
            get_shapefile(zip_file)
        the_exception = context.exception
        self.assertEqual(MISSING_FILE, the_exception.message)

    def test_missing_shx(self):
        """
        Test missing .shx file
        """
        path = os.path.join(BASE_DIR, "tests", "fixtures", "missing_shx.zip")
        zip_file = zipfile.ZipFile(path)

        with self.assertRaises(MissingFiles) as context:
            get_shapefile(zip_file)
        the_exception = context.exception
        self.assertEqual(MISSING_FILE, the_exception.message)

    @override_settings(TASKING_CHECK_NUMBER_OF_FILES_IN_SHAPEFILES_DIR=True)
    def test_missing_files(self):
        """
        Test MissingFiles error message is what we expect
        """
        path = os.path.join(BASE_DIR, "tests", "fixtures", "test_missing_files.zip")
        zip_file = zipfile.ZipFile(path)

        with self.assertRaises(MissingFiles) as context:
            get_shapefile(zip_file)
        the_exception = context.exception
        self.assertEqual(MISSING_FILE, the_exception.message)

    @override_settings(TASKING_CHECK_NUMBER_OF_FILES_IN_SHAPEFILES_DIR=True)
    def test_unnecessary_files(self):
        """
        Test UnnecessaryFiles error message is what we expect
        """
        path = os.path.join(BASE_DIR, "tests", "fixtures", "test_unnecessary_files.zip")
        zip_file = zipfile.ZipFile(path)

        with self.assertRaises(UnnecessaryFiles) as context:
            get_shapefile(zip_file)
        the_exception = context.exception
        self.assertEqual(UNNECESSARY_FILE, the_exception.message)
