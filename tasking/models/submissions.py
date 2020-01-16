# -*- coding: utf-8 -*-
"""
Module for the Task Submission model(s)
"""
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from tasking.models.base import GenericFKModel, TimeStampedModel

USER = get_user_model()


class BaseSubmission(GenericFKModel, TimeStampedModel, models.Model):
    """
    Base abstract model class for a Submission

    This class is meant to be extended to add a Submission
    to your own project. It only implements the bare minimum of
    what a Submission could be.
    """
    APPROVED = 'a'
    REJECTED = 'b'
    UNDER_REVIEW = 'c'
    PENDING = 'd'

    STATUS_CHOICES = (
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (UNDER_REVIEW, _('Under Review')),
        (PENDING, _('Pending Review'))
    )
    user = models.ForeignKey(
        USER,
        verbose_name=_('User'),
        on_delete=models.PROTECT,
        help_text=_('This represents the User.')
    )
    submission_time = models.DateTimeField(
        verbose_name=_('Submission Time'),
        help_text=_('This is the date and time the task was submitted.')
    )
    valid = models.BooleanField(
        verbose_name=_('Valid'),
        default=False,
        help_text=_('This represents whether submission is valid or not.')
    )
    status = models.CharField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES,
        default=PENDING,
        max_length=1,
        help_text=_('The status of the Submission'))
    comments = models.TextField(
        _('Comments'),
        blank=True,
        default='',
        help_text=_('This represents the comments.')
    )

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        This is the meta options class for the abstract Submission model
        """
        abstract = True


class Submission(BaseSubmission):
    """
    Submission model class
    """
    task = models.ForeignKey(
        'tasking.Task',
        verbose_name=_('Task'),
        on_delete=models.PROTECT,
        help_text=_('This represents the Task.')
    )
    location = models.ForeignKey(
        'tasking.Location',
        verbose_name=_('Location'),
        blank=True,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        help_text=_('This represents the Location.')
    )

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        This is the meta options class for the Submission model
        """
        abstract = False
        app_label = 'tasking'
        ordering = ['submission_time', 'task__name', 'id']

    def __str__(self):
        """
        String representation of a Submission object

        e.g. Cattle Price - 1 submission 1
        """
        return f'{self.task} submission {self.pk}'

    def get_approved(self, status):
        """
        Class method that gets the value of approved property
        """
        if status == self.APPROVED:
            return True
        if status == self.REJECTED:
            return False

        return None

    @property
    def approved(self):
        """
        Approved class property for submission
        """
        return self.get_approved(self.status)
