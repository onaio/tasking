"""
Module for the Task model(s)
"""
from django.db import models
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey

from tasking.models.base import GenericFKModel, TimeStampedModel
from tasking.models.managers import TaskManager
from tasking.validators import validate_rrule


class BaseTask(MPTTModel, GenericFKModel, TimeStampedModel, models.Model):
    """
    Base abstract model class for a Task

    This class is meant to be extended to add Tasks to your own project.
    It only implements the bare minimum of what a Task could be.
    """

    ACTIVE = "a"
    DEACTIVATED = "b"
    EXPIRED = "c"
    DRAFT = "d"
    SCHEDULED = "s"
    ARCHIVED = "e"

    STATUS_CHOICES = (
        (ACTIVE, _("Active")),
        (DEACTIVATED, _("Deactivated")),
        (EXPIRED, _("Expired")),
        (DRAFT, _("Draft")),
        (SCHEDULED, _("Scheduled")),
        (ARCHIVED, _("Archived")),
    )

    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent task"),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_("This represents the parent task."),
    )
    name = models.CharField(
        _("Name"), max_length=255, help_text=_("This represents the name.")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        default="",
        help_text=_("This represents the description."),
    )
    start = models.DateTimeField(
        verbose_name=_("Start"),
        help_text=_("This is the date and time the task starts."),
    )
    end = models.DateTimeField(
        verbose_name=_("End"),
        null=True,
        blank=True,
        default=None,
        help_text=_("This is the date and time the task ends."),
    )
    timing_rule = models.TextField(
        verbose_name=_("Timing Rule"),
        validators=[validate_rrule],
        null=True,
        blank=True,
        default=None,
        help_text=_("This stores the rrule for recurrence."),
    )
    total_submission_target = models.IntegerField(
        verbose_name=_("Total Submissions Target"),
        null=True,
        blank=True,
        default=None,
        help_text=_(
            "This is the total number of submissions required for this task. "
            "Set to None if there is no Max."
        ),
    )
    user_submission_target = models.IntegerField(
        verbose_name=_("User Submissions Target"),
        null=True,
        blank=True,
        default=None,
        help_text=_(
            "This is the total number of submissions per user required for "
            "this task. Set to None if there is no Max."
        ),
    )
    status = models.CharField(
        verbose_name=_("Status"),
        choices=STATUS_CHOICES,
        default=DRAFT,
        max_length=1,
        help_text=_("The status of the Task"),
    )
    estimated_time = models.DurationField(
        verbose_name=_("Estimated Time"),
        null=True,
        blank=True,
        default=None,
        help_text=_(
            "This represents the estimated time it takes to complete" " a task"
        ),
    )

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        This is the meta options class for BaseTask
        """

        abstract = True


class BaseTaskLocation(TimeStampedModel, models.Model):
    """
    BaseTaskLocation abstract model class
    """

    timing_rule = models.TextField(
        verbose_name=_("Timing Rule"),
        validators=[validate_rrule],
        help_text=_("This stores the rrule for recurrence."),
    )
    start = models.TimeField(_("Start Time"))
    end = models.TimeField(_("End Time"))

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for BaseTaskLocation
        """

        abstract = True


class TaskLocation(BaseTaskLocation):
    """
    Provides extra information on Task-Location relationship
    """

    task = models.ForeignKey("tasking.Task", on_delete=models.CASCADE)
    location = models.ForeignKey("tasking.Location", on_delete=models.CASCADE)

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskLocation
        """

        abstract = False
        app_label = "tasking"
        ordering = ["task", "location", "start"]

    def __str__(self):
        """
        String representation of a TaskLocation object
        """
        return f"{self.task.name} at {self.location.name}"


class Task(BaseTask):
    """
    Task model class
    """

    segment_rules = models.ManyToManyField(
        "tasking.SegmentRule", verbose_name=_("Segment Rules"), blank=True, default=None
    )
    locations = models.ManyToManyField(
        "tasking.Location",
        through="tasking.TaskLocation",
        verbose_name=_("Locations"),
        blank=True,
        default=None,
        help_text=_("This represents the locations."),
    )

    # Custom Manager that has submission_count field
    with_submission_count = TaskManager()

    # pylint: disable=no-self-use
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        This is the meta options class for the Task model
        """

        abstract = False
        app_label = "tasking"
        ordering = ["start", "name", "id"]

    def __str__(self):
        """
        String representation of a Task object

        e.g. Cow prices - 1
        """
        return f"{self.name} - {self.pk}"

    # pylint: disable=no-member
    def get_submissions(self) -> int:
        """
        Custom method to get number of submissions
        """
        return self.submission_set.count()

    @property
    def submissions(self) -> int:
        """
        Number of Submissions made for this task
        """
        return self.get_submissions()
