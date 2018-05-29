"""
Module for the Project model
"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from tasking.models.base import GenericFKModel, TimeStampedModel


class BaseProject(GenericFKModel, TimeStampedModel, models.Model):
    """
    Base abstract model class for a Project

    This class is meant to be extended to add Projects to your own project.
    It only implements the bare minimum of what a Project could be.
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('This is the name of the Project'))

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        The meta option class for BaseProject
        """
        abstract = True


@python_2_unicode_compatible
class Project(BaseProject):
    """
    Project model class
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
        This is the meta options class for the Project model
        """
        abstract = False
        ordering = ['name']
        app_label = 'tasking'

    def __str__(self):
        """
        String representation of a Project object

        e.g. Livestock prices
        """
        return self.name
