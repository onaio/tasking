# Task

## BaseTask
Abstract class for Tasks.  
Inherits:
```
MPTTModel
GenericFKModel
TimeStampedModel
models.Model
```

---
  * parent `TreeForeignKey` -
  * name `CharField` -
  * description `TextField` -
  * start `DateTimeField` -
  * end `DateTimeField` -
  * timing_rule `TextField` -
  * total_submission_target `IntegerField` -
  * user_submission_target `IntegerField` -
  * status `CharField` -


## Task
Concrete class for Tasks  
Inherits
```
BaseTask
```

---
  * segment_rules `ManyToManyField` -
  * segment_rules `ManyToManyField` -
