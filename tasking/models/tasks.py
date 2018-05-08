# -*- coding: utf-8 -*-
"""
Module for the Task model(s)
"""
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible


class BaseTask(models.Model):
    """
    Base abstract model class for a Task

    This class is meant to be extended to add Tasks to your own project.
    It only implements the bare minimum of what a Task could be.
    """
    ACTIVE = 'a'
    DRAFT = 'b'
    CLOSED = 'c'

    STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (DRAFT, _('Draft')),
        (CLOSED, 'Closed'),
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_('Parent task'),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_('This represents the parent task.'))
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('This represents the name.'))
    description = models.TextField(
        _('Description'),
        blank=True,
        default='',
        help_text=_('This represents the description.'))
    tasklist_id = models.ForeignKey(
        'tasking.BaseTaskList',
        verbose_name=_('Task List'),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_('This represents the tasklist.'))
    location_id = models.ForeignKey(
        'tasking.BaseLocation',
        verbose_name=_('Location'),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_('This represents the location.'))
    start = models.DateTimeField(
        verbose_name=_('Start'),
        help_text=_('This is the date and time the task starts.')
        )
    end = models.DateTimeField(
        verbose_name=_('Start'),
        null=True,
        blank=True,
        default=None,
        help_text=_('This is the date and time the task starts.')
        )
    timing_rule = models.TextField(
        verbose_name=_('Timing Rule'),
        help_text=_('This stores the rrule for recurrence.'))
    total_submission_target = models.IntegerField(
        verbose_name=_('Total Submissions Target'),
        null=True,
        blank=True,
        default=None,
        help_text=_(
            'This is the total number of submissions required for this task. '
            'Set to None if there is no Max.'))
    user_submission_target = models.IntegerField(
        verbose_name=_('User Submissions Target'),
        null=True,
        blank=True,
        default=None,
        help_text=_(
            'This is the total number of submissions per user required for '
            'this task. Set to None if there is no Max.'))
    status = models.CharField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES,
        default=DRAFT,
        max_length=1,
        help_text=_('The status of the Task'))

    # pylint: disable=no-self-use
    class Meta(object):
        """
        This is the meta options class for BaseTask
        """
        abstract = True


@python_2_unicode_compatible
class Task(BaseTask):
    """
    Task model class
    """
    pass

    # pylint: disable=no-self-use
    class Meta(object):
        """
        This is the meta options class for the Task model
        """
        abstract = False
        ordering = ['start', 'tasklist_id', 'name', 'id']

    def __str__(self):
        """
        String representation of a Task object

        e.g. Cow prices - 1
        """
        return "{name} - {pk}".format(pk=self.pk, name=self.name)
