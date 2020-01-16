# Segment Rules

A segment in this case is ...
A segment rule therefore...

## BaseSegmentRule
Inherits:
```
TimeStampedModel
django.db.Model
```

  * name `CharField` - _required_ name of the rule
  * description `TextField` - description of the rule
  * target_content_type `ForeignKey` -
  * target_field `CharField` -
  * target_field_value `CharField` -
  * active `BooleanField` - yes or no value whether the segment rule is active


## SegmentRule
Inherits:
```
BaseSegmentRule
```
