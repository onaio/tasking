"""
Tasking validators
"""
from dateutil.rrule import rrulestr


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
