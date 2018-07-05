# Task occurences
A table to store a pre-computed enumeration of task events
Computed from an [rrule](https://www.ietf.org/rfc/rfc2445.txt).

## BaseOccurence


---
  * date `DateField` - the date
  * start_time `TimeField` - the start time
  * end_time `TimeField` - the end time


## TaskOccurence


---
  * task `ForeignKey` - the task id
  * location `ForeignKey` - the location id


#### methods
`get_timestring`:  Returns a nice human-readable string that represents that date, start and end time.

