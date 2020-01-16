"""
Custom exceptions for tasking
"""
from tasking.common_tags import (INVALID_SHAPEFILE, MISSING_FILE, NO_SHAPEFILE,
                                 TARGET_DOES_NOT_EXIST, UNNECESSARY_FILE)


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


class InvalidShapeFile(Exception):
    """
    Custom Exception raised when the shapefile is not valid
    """

    message = INVALID_SHAPEFILE


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
