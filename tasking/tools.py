# -*- coding: utf-8 -*-
"""
Tools for tasking
"""
from __future__ import unicode_literals

import operator
from datetime import time
from functools import reduce

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from dateutil.rrule import rrulestr

from tasking.models import TaskOccurrence
from tasking.utils import get_rrule_end, get_rrule_start

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
BULK_CREATE_OCCURRENCES = getattr(
    settings, 'TASKING_BULK_CREATE_OCCURRENCES', True)


def get_allowed_contenttypes(allowed_content_types=ALLOWED_CONTENTTYPES):
    """
    Returns a queryset of allowed content_types
    """
    filters = [Q(app_label=item['app_label'], model=item['model']) for item in
               allowed_content_types]
    if filters:
        return ContentType.objects.filter(reduce(operator.or_, filters))
    return ContentType.objects.none()


def generate_task_occurrences(task):
    """
    Generates TaskOccurrence objects using the Task timing_rule field

    It works this way:
        - gets the start_time from the timing_rule
        - only generates a maximum og MAX_OCCURRENCES
        - the end time is always 23:59:59
            * the very last task occurrence will have the same end_time as
              the end_time from the timing_rule
        - occurrences with the same setart_time and end_time will not be
          created, they will be skipped silently
        - only works for valid rrules

    Returns a Queryset of TaskOccurrences
    """
    # get the rrule
    try:
        task_rrule = rrulestr(task.timing_rule)
    except ValueError:
        # not valid rrule string
        # pylint: disable=no-member
        return TaskOccurrence.objects.none()
    except TypeError:
        # not a string
        # pylint: disable=no-member
        return TaskOccurrence.objects.none()

    # get the max occurrences we can make right now
    occurrence_count = min(task_rrule.count(), MAX_OCCURRENCES)

    # the start time is always taken from the timing_rule
    start_time = get_rrule_start(task_rrule)

    # the end time from the timing_rule
    end_time = get_rrule_end(task_rrule)

    # if creating in bulk we'll use a list to keep track of occurrences
    if BULK_CREATE_OCCURRENCES:
        occurrence_list = []

    # lets loop through all datetimes in the rrule
    for rrule_instance in task_rrule:

        # if we've reached our max count then break the loop
        if len(occurrence_list) == occurrence_count:
            break

        # the end time for all but the last occurrence is the end of the day
        # this is because we have no information about what time the task
        # should run to on a particular day, we therefore set it to the end
        # of the day
        this_end_time = time(hour=23, minute=59, second=59, microsecond=999999)

        # for the last occurrence the end time is as set in timing_rule
        # this is because we believe that the task must end no later than the
        # timing_rule dictates
        if len(occurrence_list) + 1 == occurrence_count:
            this_end_time = end_time

        # do nothing unless start_time != end_time
        # we compare just the hour and minute values because ... well :)
        if (start_time.hour, start_time.minute) !=\
                (this_end_time.hour, this_end_time.minute):
            # define the TaskOccurrence object
            occurrence_obj = TaskOccurrence(
                task=task,
                date=rrule_instance.date(),
                start_time=start_time,
                end_time=this_end_time
            )

            # save it or add it to our bulk creation list
            if not BULK_CREATE_OCCURRENCES:
                occurrence_obj.save()

            occurrence_list.append(occurrence_obj)

    # bulk create occurrences if that is what we are doing
    if BULK_CREATE_OCCURRENCES and occurrence_list:
        # pylint: disable=no-member
        TaskOccurrence.objects.bulk_create(occurrence_list)

    # refresh the task object
    task.refresh_from_db()

    # return the task occurrences
    return task.taskoccurrence_set.all()
