# -*- coding: utf-8 -*-
"""
Module for the Location model(s)
"""
from __future__ import unicode_literals

from django_countries.fields import CountryField
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from tasking.models.base import GeoTimeStampedModel


class BaseLocation(MPTTModel, GeoTimeStampedModel, models.Model):
    """
    Base abstract model class for a Location

    This class is meant to be extended to add Location to your own project.
    It only implements the bare minimum of what a Location could be.
    """
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        related_name=_('children'))
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('This represents the name of Location.'))
    country = CountryField(
        _('Country'),
        blank=True,
        default='',
        help_text=_('This represents the Country.'))
    geopoint = models.PointField(
        _('GeoPoint'),
        null=True,
        blank=True,
        default=None,
        help_text=_('This represents the Geographical Point of the Location.'))
    radius = models.DecimalField(
        verbose_name=_('Radius'),
        null=True,
        blank=True,
        default=None,
        decimal_places=4,
        max_digits=64,
        help_text=_('This represents the radius from the geopoint.'))
    shapefile = models.MultiPolygonField(
        srid=4326,
        verbose_name=_('Shapefile'),
        null=True,
        blank=True,
        default=None,
        help_text=_('This represents the Shapefile of the Location'))

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        This is the meta options class for the abstract Location model
        """
        abstract = True

    class MPTTMeta:
        """
        This is the MPTTMeta options class for the abstract Location model
        """
        order_insertion_by = ['id']


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
        ordering = ['country', 'name', 'id']

    # pylint: disable=no-else-return
    def __str__(self):
        """
        String representation of a Location object

        e.g. Kenya - Nairobi
        """
        if self.country.name != '':
            return "{country} - {name}".format(
                country=self.country.name,
                name=self.name)
        else:
            return "{name}".format(
                name=self.name)
