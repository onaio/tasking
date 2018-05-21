# -*- coding: utf-8 -*-
"""
Custom exceptions for tasking
"""
from __future__ import unicode_literals

from tasking.common_tags import TARGET_DOES_NOT_EXIST, NO_SHAPEFILE
from tasking.common_tags import MISSING_FILE, UNNECESSARY_FILE


class TargetDoesNotExist(Exception):
    """
    Custom Exception raised when the target type does not exist
    """

    message = TARGET_DOES_NOT_EXIST


class ShapeFileNotFound(Exception):
    """
    Custom Exception raised when the shapefile is not found
    """

    message = NO_SHAPEFILE


class MissingFiles(Exception):
    """
    Custom Exception raised when a file is missing for shapefile
    """

    message = MISSING_FILE


class UnnecessaryFiles(Exception):
    """
    Custom Exception raised when a zipfile exceeds needed files
    """

    message = UNNECESSARY_FILE
