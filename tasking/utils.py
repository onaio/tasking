# -*- coding: utf-8 -*-
"""
Utility functions for tasking
"""
from __future__ import unicode_literals

from dateutil.rrule import rrulestr


def validate_rrule(rule_string):
    """
    Validates an rrule string; returns True or False
    """
    try:
        rrulestr(rule_string)
    except ValueError as exc:
        # this string is not a valid rrule
        return False
    except TypeError as exc:
        # this is not even a string
        return False
    else:
        return True
