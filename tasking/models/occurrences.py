# -*- coding: utf-8 -*-
"""
Occurrence models module
"""
from __future__ import unicode_literals

from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from tasking.models.base import TimeStampedModel


class BaseOccurrence(TimeStampedModel, models.Model):
    """
    Occurrence abstract model class
    """
    date = models.DateField(_('Date'),
                            help_text=_('The date of the occurrence'))
    start_time = models.TimeField(
        _('Start Time'),
        help_text=_('The start time of the occurrence'))
    end_time = models.TimeField(
        _('End Time'),
        help_text=_('The end time of the occurrence')
    )

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta for BaseOccurrence
        """
        abstract = True


@python_2_unicode_compatible
class TaskOccurrence(BaseOccurrence):
    """
    TaskOccurrence model class
    """
    task = models.ForeignKey(
        'tasking.Task',
        verbose_name=_('Task Occurrence'),
        on_delete=models.CASCADE
    )

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta for TaskOccurrence
        """
        abstract = False
        ordering = ['task', 'date', 'start_time']

    def __str__(self):
        """
        Returns string representation of the object
        """
        return '{} - {}'.format(self.task, self.get_timestring())

    def get_timestring(self):
        """
        Returns a nice human-readable string that represents that date, start
        and end time
        """
        date_format_obj = DateFormat(self.date)
        start_format_obj = DateFormat(self.start_time)
        end_format_obj = DateFormat(self.end_time)

        return '{date}, {start} to {end}'.format(
            date=date_format_obj.format('jS F Y'),
            start=start_format_obj.format('P'),
            end=end_format_obj.format('P')
        )
