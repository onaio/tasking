# Base

Abstract classes needed by other models in Kaznet.

## GeoTimeStampedModel

GeoDjango models reexports DateTimeField from django models but we still create a GeoTimeStampedModel so that inheriting classes can inherit other GeoDjango model fields and APIs.

---
  * created `DateTimeField` - _auto added_ creation date and time for a record
  * modified `DateTimeField` - _auto added_ modification  last modified date and time for a record


## TimeStampedModel
Abstract class to provide creation and modification datetimes for records in subclasses.

---
  * created `DateTimeField` - _auto added_ creation date and time for a record
  * modified `DateTimeField` - _auto added_ modification  last modified date and time for a record


## GenericFKModel
Generic class to DRY out references to other models.

---
  * target_content_type `ForeignKey` -
  * target_object_id `PositiveIntegerField` -
  * target_content_object `GenericForeignKey` - actual foreign key reference to another model
