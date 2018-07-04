# -*- coding: utf-8 -*-
"""
Signals for tasking

These signals are not connected by default, you will have to connect them
'manually' in your own code
"""
from __future__ import unicode_literals

from tasking.utils import generate_task_occurrences


# pylint: disable=unused-argument
def create_occurrences(sender, instance, created, **kwargs):
    """
    Create occurrences when a task timing_rule changes
    """
    if instance.timing_rule:
        # delete any existing occurrences
        instance.taskoccurrence_set.all().delete()
        # generate new occurrences
        generate_task_occurrences(
            task=instance, timing_rule=instance.timing_rule)
