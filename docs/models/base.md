# Base

Abstract classes needed by other models in Kaznet.

## GeoTimeStampedModel
Re-export timestamp model from django model as well as other geo django apis and fields.  
Inherits:
```
django.contrib.gis.db.Models
```

---
  * created `DateTimeField` - _auto added_ creation date and time for a record
  * modified `DateTimeField` - _auto added_ modification  last modified date and time for a record


## TimeStampedModel
Abstract class to provide creation and modification datetimes for records in subclasses.  
Inherits:
```
django.db.models
```

---
  * created `DateTimeField` - _auto added_ creation date and time for a record
  * modified `DateTimeField` - _auto added_ modification  last modified date and time for a record


## GenericFKModel
Generic class to DRY out references to other models.  
Inherits:
```
django.db.models
```

---
  * target_content_type `ForeignKey` -
  * target_object_id `PositiveIntegerField` -
  * target_content_object `GenericForeignKey` - actual foreign key reference to another model
