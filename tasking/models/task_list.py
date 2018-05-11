"""
Module for the Task List model
"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


class BaseTaskList(models.Model):
    """
    Base abstract model class for a Task List

    This class is meant to be extended to add Task Lists to your own project.
    It only implements the bare minimum of what a Task List could be.
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('This is the name of the task list'))

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        The meta option class for BaseTaskList
        """
        abstract = True


@python_2_unicode_compatible
class TaskList(BaseTaskList):
    """
    Task list model class
    """
    tasks = models.ManyToManyField(
        'tasking.Task',
        verbose_name=_('Tasks'),
        blank=True,
        default=None,
        help_text=_('This represents the Task.'))

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Task List model
        """
        abstract = False
        ordering = ['name']

    def __str__(self):
        """
        String representation of a Task List object

        e.g. Livestock prices
        """
        return self.name
