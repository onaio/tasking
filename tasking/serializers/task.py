"""
Tasking Serializers
"""
from dateutil.rrule import rrulestr
from rest_framework import serializers

from tasking.common_tags import (
    INVALID_END_DATE,
    INVALID_START_DATE,
    INVALID_TIMING_RULE,
    MISSING_START_DATE,
)
from tasking.models import Task, TaskLocation
from tasking.serializers.base import GenericForeignKeySerializer
from tasking.utils import get_rrule_end, get_rrule_start
from tasking.validators import validate_rrule


def check_timing_rule(value):
    """
    Validate timing rule
    """
    if validate_rrule(value) is True:
        return value
    raise serializers.ValidationError(INVALID_TIMING_RULE)


class TaskLocationSerializer(serializers.ModelSerializer):
    """
    TaskLocation serialzier class
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskLocationSerializer
        """

        model = TaskLocation
        fields = [
            "task",
            "created",
            "modified",
            "location",
            "timing_rule",
            "start",
            "end",
        ]

    # pylint: disable=no-self-use
    def validate_timing_rule(self, value):
        """
        Validate timing rule
        """
        return check_timing_rule(value)


class TaskLocationCreateSerializer(TaskLocationSerializer):
    """
    Serializer model class used when creating a TaskLocation object
    during Task creation
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskLocationSerializer
        """

        model = TaskLocation
        # we dont include the task field as it will be added in TaskSerializer
        fields = ["location", "timing_rule", "start", "end"]

    def to_representation(self, instance):
        """
        Use TaskLocationSerializer when reading the object
        """
        return TaskLocationSerializer(instance).data


class TaskSerializer(GenericForeignKeySerializer):
    """
    Task serializer class
    """

    start = serializers.DateTimeField(required=False)
    submission_count = serializers.SerializerMethodField()
    locations_input = TaskLocationCreateSerializer(
        many=True, required=False, write_only=True
    )
    task_locations = serializers.SerializerMethodField(read_only=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TaskSerializer
        """

        fields = [
            "id",
            "created",
            "modified",
            "name",
            "parent",
            "estimated_time",
            "description",
            "start",
            "end",
            "timing_rule",
            "total_submission_target",
            "user_submission_target",
            "status",
            "submission_count",
            "target_content_type",
            "target_id",
            "segment_rules",
            "locations",
            "locations_input",
            "task_locations",
        ]
        read_only_fields = ["locations"]
        model = Task

    # pylint: disable=no-self-use
    def validate_timing_rule(self, value):
        """
        Validate timing rule
        """
        return check_timing_rule(value)

    def validate(self, attrs):
        """
        Object level validation method for TaskSerializer
        """
        if not self.instance:
            # this is a new object

            # get start from input
            start_from_input = attrs.get("start")

            # get timing rules from task locations
            tasklocation_timing_rules = []
            for location_input in attrs.get("locations_input", []):
                tasklocation_timing_rules.append(location_input["timing_rule"])

            # get start and end from timing rules
            timing_rule = attrs.get("timing_rule")
            if timing_rule is not None:
                timing_rule_start = get_rrule_start(rrulestr(timing_rule))
                timing_rule_end = get_rrule_end(rrulestr(timing_rule))
            else:
                timing_rule_start = None
                timing_rule_end = None

            if not start_from_input:
                # start was not input by user, we try and generate it from
                # timing rules
                if not timing_rule_start:
                    # we cannot determine a start time
                    raise serializers.ValidationError(
                        {"timing_rule": MISSING_START_DATE, "start": MISSING_START_DATE}
                    )

                attrs["start"] = timing_rule_start

            # get end
            attrs["end"] = attrs.get("end", timing_rule_end)

        # If end date is present we validate that it is greater than start_date
        if attrs.get("end") is not None:
            # If end date is lesser than the start date raise an error
            the_start = attrs.get("start")
            if the_start is None and self.instance is not None:
                the_start = self.instance.start

            if not the_start:
                raise serializers.ValidationError({"start": INVALID_START_DATE})

            if attrs["end"] < the_start:
                raise serializers.ValidationError({"end": INVALID_END_DATE})

        # If start date is present and this is an existing object, we validate
        # that the start date is not greater than the existing end date
        if (  # pylint: disable=bad-continuation
            attrs.get("start") is not None
            and self.instance is not None
            and self.instance.end is not None
            and attrs.get("start") > self.instance.end
        ):
            raise serializers.ValidationError({"start": INVALID_START_DATE})

        return super(TaskSerializer, self).validate(attrs)

    def get_submission_count(self, obj):
        """
        Add a custom method to get submission count
        """
        try:
            return obj.submission_count
        except AttributeError:
            return obj.submissions

    def get_task_locations(self, obj):
        """
        Get serialized TaskLocation objects
        """
        # pylint: disable=no-member
        queryset = TaskLocation.objects.filter(task=obj)
        return TaskLocationSerializer(queryset, many=True).data

    def create(self, validated_data):
        """
        Custom create method for Tasks
        """
        locations_data = validated_data.pop("locations_input", [])

        task = super(TaskSerializer, self).create(validated_data=validated_data)

        for location_data in locations_data:
            location_data["task"] = task
            TaskLocationSerializer.create(
                TaskLocationSerializer(), validated_data=location_data
            )

        return task

    def update(self, instance, validated_data):
        """
        Custom update method for Tasks
        """
        locations_data = validated_data.pop("locations_input", [])
        task = super(TaskSerializer, self).update(
            instance=instance, validated_data=validated_data
        )

        # we assume that this is the one final list of locations to be
        # linked to this task and that other relationships should be removed
        # if task_locations is empty it means the user is removing all Task and
        # Location relationships

        # pylint: disable=no-member
        TaskLocation.objects.filter(task=task).delete()

        for location_data in locations_data:
            location_data["task"] = task
            TaskLocationSerializer.create(
                TaskLocationSerializer(), validated_data=location_data
            )

        return task
