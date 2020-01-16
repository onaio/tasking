# Projects

Projects hold tasks within an organization. You can think of them as folders/directories.

## BaseProject
Abstract class for projects

Inherits:
```
```

---
  * name `CharField` - name of the project


## Project
Concrete class implementing projects.
Inherits:
```
BaseProject
```

---
  * tasks `ManyToManyField` - ids of the tasks contained within the project.
