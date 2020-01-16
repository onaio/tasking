"""
Task Serializers init module
"""
from tasking.serializers.contenttype import ContentTypeSerializer  # noqa
from tasking.serializers.location import LocationSerializer  # noqa
from tasking.serializers.locationtype import LocationTypeSerializer  # noqa
from tasking.serializers.occurrence import TaskOccurrenceSerializer  # noqa
from tasking.serializers.project import ProjectSerializer  # noqa
from tasking.serializers.segment_rule import SegmentRuleSerializer  # noqa
from tasking.serializers.submissions import SubmissionSerializer  # noqa
from tasking.serializers.task import (TaskLocationSerializer,  # noqa
                                      TaskSerializer)
