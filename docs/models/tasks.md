# Task

## BaseTask
| parent | name | description | start | end | timing_rule | total_submission_target | user_submission_target | status |
| :----: | :--: | :---------: | :---: | :-: | :---------: | :---------------------: | :--------------------: | :----: |

Abstract class for Tasks

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
Inherits BaseTask


| segment_rules | locations |
| :-----------: | :-------: |

  * segment_rules `ManyToManyField` - 
   segment_rules `ManyToManyField` - 
