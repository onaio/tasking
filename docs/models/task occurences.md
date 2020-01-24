# Task occurences

Model representing when a task should occurr. Task Occurrences depict when a specific task should occur.

## BaseOccurence

Abstract model class representing an occurence.

Inherit:
```
tasking.models.base.TimeStampedModel
django.db.models.Model
```

---
  * date `DateField` - The date of occurrence.
  * start_time `TimeField` - The start time of the occurrence.
  * end_time `TimeField` - The time the occurrence ends.


## TaskOccurence

Concrete model class representing an occurence. These implementation of Occurrences is focused on documenting the occurrences of Tasks.

_Task Occurrences are pre-computed enumerations of task events computed from an [rrule](https://www.ietf.org/rfc/rfc2445.txt). The package auto generates them through signals. More info on that [here](https://github.com/onaio/tasking/blob/master/docs/models/tasks.md#signals)._

Inherit:
```
BaseOccurrence
```

---
  * task `ForeignKey` - The task that is supposed to occur.
  * location `ForeignKey` - The location / place the occurrence should happen.


### Methods

`get_timestring`: Returns a nice human-readable string that represents that date, start and end time of the occurence.

### Signals:

`create_occurrences`: A signal that generates occurrences based on the `timing_rule` tied to the sender instance.
