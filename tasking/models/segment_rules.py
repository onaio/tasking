"""
Module for SegmentRule model(s)
"""
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _

from tasking.models.base import TimeStampedModel


class BaseSegmentRule(TimeStampedModel, models.Model):
    """
    BaseSegmentRule abstract model class

    A SegmentRule is basically a way to create a dynamic filter based on
    the SegmentRule target model.

    For example, if you have this as the SegmentRule:
        target: Task
        target_field: id
        target_field_value: 6
    Then you would be able to use this SegmentRule to filter:
        SELECT * FROM task WHERE task_id=6;
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('The name of this rule.'))
    description = models.TextField(
        _('Description'),
        blank=True,
        default='',
        help_text=_('The description of this rule.')
    )
    target_content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='segment_rule',
        default=None,
        db_index=True,
        on_delete=models.SET_NULL)
    target_field = models.CharField(
        _('Target Field'),
        max_length=255,
        help_text=_('The field on the target model.'),
        db_index=True
    )
    target_field_value = models.CharField(
        _('Target Field Value'),
        max_length=255,
        help_text=_('The value of the target field')
    )
    active = models.BooleanField()

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for BaseSegmentRule
        """
        abstract = True


class SegmentRule(BaseSegmentRule):
    """
    SegmentRule model class
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for SegmentRule
        """
        abstract = False
        app_label = 'tasking'
        ordering = ['name']

    def __str__(self):
        return self.name
