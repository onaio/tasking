# Projects

Model used to represent projects. Projects can be a collection of things i.e tasks, locations, submissions etc.

Projects provide an easy way to categorize other objects within your application.

## BaseProject

Abstract class implementing projects

Inherits:
```
mptt.models.MPTTModel
tasking.models.base.GeoTimeStampedModel
django.db.models.Model
```

---
  * name `CharField` - _required_ Name of the project.


## Project

Concrete class for projects. This implementation of projects is more focused towards a collection of tasks.

Inherits:
```
BaseProject
```

---
  * tasks `ManyToManyField` - All tasks stored in the project.
