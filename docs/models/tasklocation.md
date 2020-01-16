# TaskLocation

This is a many-to-many "through" model that is used to store extra information on the relationship between `Task` and `Location` objects.

  - `task`: *integer*, is a foreign key to a Task object
  - `location`: *integer*, is a foreign key to a Location object
  - `start`: *TimeField*, the start time
  - `end`": *TimeField*, the end time
  - `timing_rule`: *TextField*, [recurrence rule](https://tools.ietf.org/html/rfc2445)
