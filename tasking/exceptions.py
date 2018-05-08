# -*- coding: utf-8 -*-
"""
Custom exceptions for tasking
"""
from __future__ import unicode_literals

from tasking.common_tags import TARGET_DOES_NOT_EXIST


class TargetDoesNotExist(Exception):
    """
    Custom Exception raised when the target type does not exist
    """

    message = TARGET_DOES_NOT_EXIST
