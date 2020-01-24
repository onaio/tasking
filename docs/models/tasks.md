# Task

Model representing a task

## BaseTask
Abstract model class implementing tasks.

> The start and end are best generated from the rrule and saved for efficiency seems redundant to expose them in your API.

Inherits:
```
mptt.models.MPTTModel
tasking.models.base.GenericFKModel
tasking.models.base.TimeStampedModel
django.db.models.Model
```

---
  * parent `TreeForeignKey` - A link the parent task.
  * name `CharField` - _required_ Name of the task.
  * description `TextField` - The tasks description.
  * start `DateTimeField` - The date and time this task should start.
  * end `DateTimeField` - The date and time this task should end.
  * timing_rule `TextField` - [Recurrence rule](https://tools.ietf.org/html/rfc2445) for the task.
  * estimated_time `DurationField` - An estimate of the amount of time this task will take.
  * total_submission_target `IntegerField` - Maximum number of submissions this task should receive from all users.
  * user_submission_target `IntegerField` - Maximum number of submissions a particular user can make for this task.
  * status `CharField` - The status of the task. Has to be one of:
    - active
    - deactivated
    - expired
    - draft
    - scheduled
    - archived


## Task

Concrete model class implementing Tasks. This implementation of tasks is focused on implementing a way to limit a task to specific locations and apply rules onto a task.

Inherits:
```
BaseTask
```

---
  * segment_rules `ManyToManyField` - [Segment rules](./segment%20rules.md) you want to associate the task with.
  * locations `ManyToManyField` - The locations that this task should be completed/done in.

### Methods:

`get_submissions`: Returns the number of submissions made for a Task. Sets the value for the `submissions` property.

### Properties:

`submissions`: *Integer*, number of submissions.
