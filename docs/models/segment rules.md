# Segment Rules :: BETA

Model representing a segment rule. A segment rule is a way to create dynamic filters based on a particular target.

_This feature is still being worked on_

## BaseSegmentRule

Abstract class implementing segment rules.

Inherits:
```
tasking.models.base.TimeStampedModel
django.db.models.Model
```

  * name `CharField` - _required_ Name of the segment rule.
  * description `TextField` - Description of the segment rule.
  * target_content_type `ForeignKey` - The target of which this segment rule should act upon.
  * target_field `CharField` - Field within the target that the segment rule filters. i.e 'task_id'
  * target_field_value `CharField` - The filtering value of the target field. i.e 'task_id': '1'
  * active `BooleanField` - _required_ Whether the segment rule is actively affecting the target.


## SegmentRule

Concrete class implementing segment rules. Concretely implements `BaseSegmentRule` as is.

Inherits:
```
BaseSegmentRule
```
