"""
Base Tasking Models
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as geomodels
from django.db import models
from django.utils.translation import ugettext as _


class GeoTimeStampedModel(geomodels.Model):
    """
    Abstract model class that includes geo timestamp fields
    """

    created = geomodels.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    modified = geomodels.DateTimeField(verbose_name=_("Modified"), auto_now=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for GeoTimeStampedModel
        """

        abstract = True


class TimeStampedModel(models.Model):
    """
    Abstract model class that includes timestamp fields
    """

    created = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_("Modified"), auto_now=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TimeStampedModel
        """

        abstract = True


class GenericFKModel(models.Model):
    """
    Abstract model class that includes a generic foreign key
    """

    target_content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        default=None,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    target_object_id = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default=None
    )
    target_content_object = GenericForeignKey("target_content_type", "target_object_id")

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for GenericFKModel
        """

        abstract = True
