# -*- coding: utf-8 -*-
"""
Module for SegmentRule model(s)
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


class BaseSegmentRule(models.Model):
    """
    BaseSegmentRule abstract model class

    A SegmentRule is basically a way to create a dynamic filter based on
    the SegmentRule target model.

    For example, if you have this as the SegmentRule:
        target: Task
        target_field: id
        target_field_value: 6
    Then you would be able to use this SegmentRule to filter:
        where task_id is 6
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
        related_name='segment_target',
        blank=True,
        null=True,
        default=None,
        db_index=True,
        on_delete=models.SET_NULL)
    target_object_id = models.PositiveIntegerField(
        db_index=True,
        blank=True,
        null=True,
        default=None
    )
    target_content_object = GenericForeignKey(
        'target_content_type', 'target_object_id')
    active = models.BooleanField()

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for BaseSegmentRule
        """
        abstract = True


@python_2_unicode_compatible
class SegmentRule(BaseSegmentRule):
    """
    SegmentRule model class
    """

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """
        Meta options for SegmentRule
        """
        abstract = False
        ordering = ['name']

    def __str__(self):
        return self.name
