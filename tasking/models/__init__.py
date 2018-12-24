"""
Task Models init module
"""
from tasking.models.locations import BaseLocation, Location  # noqa
from tasking.models.locationtypes import BaseLocationType, LocationType  # noqa
from tasking.models.occurrences import BaseOccurrence, TaskOccurrence  # noqa
from tasking.models.projects import BaseProject, Project  # noqa
from tasking.models.segment_rules import BaseSegmentRule, SegmentRule  # noqa
from tasking.models.submissions import BaseSubmission, Submission  # noqa
from tasking.models.tasks import (BaseTask, BaseTaskLocation, Task,  # noqa
                                  TaskLocation)
