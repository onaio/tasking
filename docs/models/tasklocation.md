# Task Location

Model used to store extra information on the relationship between `Task` and `Location` objects.

_This is a many-to-many "through" model that is used to store extra information on the relationship between `Task` and `Location` objects._

# BaseTaskLocation

Abstract model class implementing Tasklocations.

Inherit:
```
tasking.models.base.TimeStampedModel
django.db.models.Model
```

___
  * timing_rule `TextField`: *required* The recurrence rule](https://tools.ietf.org/html/rfc2445).
  * start `TimeField`: *required* The start time.
  * end `TimeField`: *required* The end time.


# TaskLocation

Concrete model class implementing TaskLocations

Inherit:
```
BaseTaskLocation
```

___
  * task `ForeignKey`: *required* The task.
  * location `ForeignKey`: *required* The location.
