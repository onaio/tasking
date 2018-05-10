# -*- coding: utf-8 -*-
"""
Module for the Location model(s)
"""
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from tasking.models.base import GeoTimeStampedModel


class BaseLocation(GeoTimeStampedModel, models.Model):
    """
    Base abstract model class for a Location

    This class is meant to be extended to add Location to your own project.
    It only implements the bare minimum of what a Location could be.
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('This represents the name of Location.'))
    country = models.CharField(
        _('Country'),
        max_length=255,
        help_text=_('This represents the name of the Country.'))
    geopoint = models.PointField(
        verbose_name=_('GeoPoint'),
        null=True,
        blank=True,
        default=True,
        help_text=_('This represents the Geographical Point of the Location.'))
    radius = models.DecimalField(
        verbose_name=_('Radius'),
        null=True,
        blank=True,
        default=None,
        help_text=_('This represents the radius of the Location.'))
    shapefile = models.MultiPolygonField(
        srid=4326,
        verbose_name=_('Shapefile'),
        null=True,
        blank=True,
        default=None,
        help_text=_('This represents the Shapefile of the Location'))


@python_2_unicode_compatible
class Location(BaseLocation):
    """
    Location model class
    """
    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the Location model
        """
        abstract = False
        ordering = ['country', 'name']

    def __str__(self):
        """
        String representation of a Location object

        e.g. Kenya - Nairobi
        """
        return "{country} - {name}".format(
            country=self.country,
            name=self.name)
