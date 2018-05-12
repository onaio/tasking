# -*- coding: utf-8 -*-
"""
Utility functions for tasking
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from dateutil.rrule import rrulestr

from tasking.exceptions import TargetDoesNotExist


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


def get_target(app_label, target_type):
    """
    Returns the target_type
    """
    try:
        return ContentType.objects.get(app_label=app_label, model=target_type)
    except ContentType.DoesNotExist:  # pylint: disable=no-member
        raise TargetDoesNotExist()
