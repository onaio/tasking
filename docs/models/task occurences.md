# Task occurences
A table to store a pre-computed enumeration of task events
Computed from an [rrule](https://www.ietf.org/rfc/rfc2445.txt). 

## BaseOccurence


---
  * date `DateField` -
  * start_time `TimeField` -
  * end_time `TimeField` -


## TaskOccurence


---
  * task `ForeignKey` -


#### methods
`get_timestring`:  Returns a nice human-readable string that represents that date, start and end time.

