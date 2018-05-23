# -*- coding: utf-8 -*-
"""
Signals for tasking
"""
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from tasking.tools import generate_task_occurrences


@receiver(post_save, sender='tasking.Task')
# pylint: disable=unused-argument
def create_occurrences(sender, instance, created, **kwargs):
    """
    Create occurrences when a task timing_rule changes
    """
    if instance.timing_rule:
        # delete any existing occurrences
        instance.taskoccurrence_set.all().delete()
        # generate new occurrences
        generate_task_occurrences(instance)
