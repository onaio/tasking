# Task

## BaseTask
Abstract class for Tasks.
> The start and end are best generated from the rrule and saved for efficiency seems redundant to expose them in your API.
Inherits:
```
MPTTModel
GenericFKModel
TimeStampedModel
models.Model
```

---
  * parent `TreeForeignKey` -
  * name `CharField` - _required_ name of the task
  * description `TextField` - a description of the task
  * start `DateTimeField` - When the task starts
  * end `DateTimeField` - When the task ends
  * timing_rule `TextField` - [recurrence rule](https://tools.ietf.org/html/rfc2445) for the task
  * total_submission_target `IntegerField` - maximum number of submissions wanted for the entire task
  * user_submission_target `IntegerField` - maximum number of submissions wanted from each enumerator 
  * status `CharField` - the status of the task. Has to be one of:  
    - active
    - deactivated
    - expired
    - draft
    - scheduled
    - archived


## Task
Concrete class for Tasks
Inherits:
```
BaseTask
```

---
  * segment_rules `ManyToManyField` - id of the [segment rule](./segment%20rules.md) you want to associate the task with
  * segment_rules `ManyToManyField` - id of the location that the task should be carried out in.

### Methods:

`get_submissions`: Returns the number of submissions made for a Task. Sets the value for the `submissions` property.

### Properties:

`submissions`: *Integer*, number of submissions.
