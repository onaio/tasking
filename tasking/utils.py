# -*- coding: utf-8 -*-
"""
Utility functions for tasking
"""
from __future__ import unicode_literals

import operator
from datetime import time
from functools import reduce

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone

from dateutil.rrule import rrulestr

from tasking.exceptions import (MissingFiles, ShapeFileNotFound,
                                TargetDoesNotExist, UnnecessaryFiles)
from tasking.models import TaskOccurrence

DEFAULT_ALLOWED_CONTENTTYPES = [
    {'app_label': 'tasking', 'model': 'task'},
    {'app_label': 'tasking', 'model': 'location'},
    {'app_label': 'tasking', 'model': 'project'},
    {'app_label': 'tasking', 'model': 'segmentrule'},
    {'app_label': 'tasking', 'model': 'submission'},
    {'app_label': 'auth', 'model': 'user'},
    {'app_label': 'auth', 'model': 'group'},
    {'app_label': 'logger', 'model': 'xform'},
    {'app_label': 'logger', 'model': 'instance'},
    {'app_label': 'logger', 'model': 'project'}
]

ALLOWED_CONTENTTYPES = getattr(settings, 'TASKING_ALLOWED_CONTENTTYPES',
                               DEFAULT_ALLOWED_CONTENTTYPES)
MAX_OCCURRENCES = getattr(settings, 'TASKING_MAX_OCCURRENCES', 500)


def get_allowed_contenttypes(allowed_content_types=ALLOWED_CONTENTTYPES):
    """
    Returns a queryset of allowed content_types
    """
    filters = [Q(app_label=item['app_label'], model=item['model']) for item in
               allowed_content_types]
    if filters:
        return ContentType.objects.filter(reduce(operator.or_, filters))
    return ContentType.objects.none()


def get_occurrence_start_time(the_rrule, start_time_input=None):
    """
    Get the start time used to create a task occurrence
    """
    if start_time_input is None:
        # the start time is always taken from the timing_rule
        # if not supplied
        start_datetime = get_rrule_start(the_rrule)
        start_time = start_datetime.time()
    else:
        start_time = start_time_input

    return start_time


def get_occurrence_end_time(task, the_rrule, end_time_input=None):
    """
    Get the end time used to create a task occurrence
    """
    end_time = None
    if end_time_input is None:
        # get the end time from the timing_rule if not supplied
        end_datetime = get_rrule_end(the_rrule)
        if end_datetime is not None:
            end_time = end_datetime.time()
        # If we dont have an end_time then we set it to be the task end time
        if end_time is None and task.end is not None:
            end_time = task.end.time()
    else:
        end_time = end_time_input

    return end_time


# pylint: disable=invalid-name
def generate_task_occurrences(
        task,
        timing_rule,
        start_time_input=None,
        end_time_input=None,
        OccurrenceModelClass=TaskOccurrence):
    """
    Generates TaskOccurrence objects using the Task timing_rule field

    It works this way:
        - gets the start_time from the timing_rule
        - only generates a maximum of MAX_OCCURRENCES
        - the end time is always 23:59:59
            * the very last task occurrence will have the same end_time as
              the end_time from the timing_rule
        - occurrences with the same start_time and end_time will not be
          created, they will be skipped silently
        - only works for valid rrules

    Returns a Queryset of OccurrenceModel class objects
    """

    # get the rrule
    try:
        the_rrule = rrulestr(timing_rule)
    except ValueError:
        # not valid rrule string
        # pylint: disable=no-member
        return OccurrenceModelClass.objects.none()
    except TypeError:
        # not a string
        # pylint: disable=no-member
        return OccurrenceModelClass.objects.none()

    # get the max occurrences we can make right now
    try:
        occurrence_count = min(the_rrule.count(), MAX_OCCURRENCES)
    except ValueError:
        occurrence_count = MAX_OCCURRENCES

    # the end datetime for the task
    task_end = task.end

    start_time = get_occurrence_start_time(
        the_rrule, start_time_input=start_time_input)

    end_time = get_occurrence_end_time(
        task, the_rrule, end_time_input=end_time_input)

    occurrence_list = []

    # lets loop through all datetimes in the rrule
    for rrule_instance in the_rrule:

        # if we've reached our max count or if rrule_instance is
        # greater than the task_end we then break the loop
        if len(occurrence_list) == occurrence_count or\
         (task_end is not None and rrule_instance.date() > task_end.date()):
            break

        # if end time is provided as in input use it as the_end_time
        if end_time_input:
            this_end_time = end_time_input
        else:
            # the end time for all but the last occurrence is the end of the
            # day this is because we have no information about what time the
            # task should run to on a particular day, we therefore set it to
            # the end of the day
            this_end_time = time(
                hour=23, minute=59, second=59, microsecond=999999)

            # for the last occurrence if the end time is not none we set the
            # end date for the timing_rule this is because we believe that
            # the task must end no later than the timing_rule dictates
            if end_time is not None:
                if len(occurrence_list) + 1 == occurrence_count:
                    this_end_time = end_time

        # do nothing unless this_end_time > start_time
        # we compare just the hour and minute values because ... well :)
        if this_end_time > start_time:
            # define the OccurrenceModelClass object
            occurrence_obj = OccurrenceModelClass(
                task=task,
                date=rrule_instance.date(),
                start_time=start_time,
                end_time=this_end_time
            )

            occurrence_list.append(occurrence_obj)

    if occurrence_list:
        # pylint: disable=no-member
        OccurrenceModelClass.objects.bulk_create(occurrence_list)

    # return the task occurrences
    return OccurrenceModelClass.objects.filter(task=task)


def generate_tasklocation_occurrences(
        task_location, OccurrenceModelClass=TaskOccurrence):
    """
    Generates TaskOccurrence objects using the TaskLocation timing_rule field

    It works this way:
        - gets the start_time from the timing_rule
        - only generates a maximum of MAX_OCCURRENCES
        - occurrences with the same start_time and end_time will not be
          created, they will be skipped silently
        - only works for valid rrules

    Returns a Queryset of OccurrenceModel class objects
    """
    return generate_task_occurrences(
        task=task_location.task,
        timing_rule=task_location.timing_rule,
        start_time_input=task_location.start,
        end_time_input=task_location.end,
        OccurrenceModelClass=OccurrenceModelClass)


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
        # we must strip the time because we should only infer the date
        # when using count, we set it to the very end of the day
        end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
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

    if settings.CHECK_NUMBER_OF_FILES_IN_SHAPEFILES_DIR:
        # Check if zipfile has more than 3 files
        if len(name_list) > 3:
            # Raise UnnecessaryFiles Exception if files exceed 3
            raise UnnecessaryFiles()
        # Check if zipfile has less than the 3 required files
        elif len(name_list) < 3:
            # Raise MissingFiles Exception
            raise MissingFiles()

    needed_files = {}

    for item in name_list:
        if item.endswith('shp'):
            needed_files['shp'] = item
        elif item.endswith('dbf'):
            needed_files['dbf'] = item
        elif item.endswith('shx'):
            needed_files['shx'] = item

    if not needed_files.get('dbf') or not needed_files.get('shx'):
        raise MissingFiles()

    if not needed_files.get('shp'):
        raise ShapeFileNotFound()

    return needed_files['shp']
