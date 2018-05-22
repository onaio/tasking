# -*- coding: utf-8 -*-
"""
Utility functions for tasking
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from django.utils import timezone
from dateutil.rrule import rrulestr

from tasking.exceptions import TargetDoesNotExist, ShapeFileNotFound
from tasking.exceptions import MissingFiles, UnnecessaryFiles


def validate_rrule(rule_string):
    """
    Validates an rrule string; returns True or False
    """
    try:
        rrulestr(rule_string)
    except ValueError:
        # this string is not a valid rrule
        return False
    except TypeError:
        # this is not even a string
        return False
    else:
        return True


def get_rrule_start(rrule_obj):
    """
    Returns the timezone-aware start datetime from rrule
    """
    # pylint: disable=protected-access
    start = rrule_obj._dtstart
    if timezone.is_naive(start):
        return timezone.make_aware(start)
    return start


def get_rrule_end(rrule_obj):
    """
    Returns the timezone-aware end datetime from rrule
    """
    # pylint: disable=protected-access
    until = rrule_obj._until
    # pylint: disable=protected-access
    count = rrule_obj._count

    if until is not None:
        # if until is set let us use it
        end = until
    elif count is not None:
        # if count is set instead we use the last ocurrence
        end = rrule_obj[-1]  # might be slow if many occurrences
    else:
        return None

    # make end timezone-aware
    if timezone.is_naive(end):
        return timezone.make_aware(end)
    return end


def get_target(app_label, target_type):
    """
    Returns the target_type
    """
    try:
        return ContentType.objects.get(app_label=app_label, model=target_type)
    except ContentType.DoesNotExist:  # pylint: disable=no-member
        raise TargetDoesNotExist()


def get_shapefile(geofile):
    """
    Returns the filename of ShapeFile
    """
    # Takes the inputted geofile(zipfile) and lists all items in it
    name_list = geofile.namelist()
    # Initializes name variable
    name = None

    # Check if zipfile has more than 3 files
    if len(name_list) > 3:
        # Raise UnnecessaryFiles Exception if files exceed 3
        raise UnnecessaryFiles()
    # Check if zipfile has less than the 3 required files
    elif len(name_list) < 3:
        # Raise MissingFiles Exeption if it has less than the required files
        raise MissingFiles()
    # Check if zipfile has 3 files only
    elif len(name_list) == 3:
        # Iterate through the names of items to find the .shp file
        for item in name_list:
            # Split the elements of the name_list in order to have an array
            # Of filename and extension name
            arr = item.split('.')
            # Check if the extension of the file is .shp
            if arr[1] == 'shp':
                # Set name to the name of the .shp file
                name = '.'.join(arr)
    # Check if name has changed from its initial value
    if name is None:
        # Raise ShapeFileNotFound exception if name hasn't changed from initial
        raise ShapeFileNotFound()
    else:
        # Return name
        return name
