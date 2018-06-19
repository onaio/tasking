"""
Module for the LocationType model
"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from tasking.models.base import TimeStampedModel


class BaseLocationType(TimeStampedModel, models.Model):
    """
    Base abstract model class for a LocationType

    This class is meant to be extended to add LocationType to your own project.
    It only implements the bare minimum of what a LocationType could be.
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('This is the name of the Location Type'))

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        The meta option class for BaseLocationType
        """
        abstract = True


@python_2_unicode_compatible
class LocationType(BaseLocationType):
    """
    LocationType model class
    """
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the LocationType model
        """
        abstract = False
        app_label = 'tasking'
        ordering = ['name', 'id']

    def __str__(self):
        """
        String representation of a LocationType object

        e.g. Waterfront
        """
        return self.name
