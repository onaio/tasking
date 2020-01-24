# Base

Abstract classes needed by other models in Ona Tasking.

## TimeStampedModel

Abstract model class that provides the `created` and `modified` datetimes for records.

Inherits:
```
django.db.models
```

---
  * created `DateTimeField` - _auto added_ The date and time the record was created.
  * modified `DateTimeField` - _auto added_ The date and time the record was last modified.

## GeoTimeStampedModel

Abstract model class that re-exports the TimeStampedmodel with GeoDjango APIs and fields.

Inherits:
```
django.contrib.gis.db.Models
```

---
  * created `DateTimeField` - _auto added_ The date and time the record was created.
  * modified `DateTimeField` - _auto added_ The date and time the record was last modified.


## GenericFKModel

Generic class to DRY out references to other models.
We use [django's contenttypes framework](https://docs.djangoproject.com/en/2.0/ref/contrib/contenttypes)
to create [generic relations](https://docs.djangoproject.com/en/2.0/ref/contrib/contenttypes/#generic-relations)
with models which don't exist yet.

Inherits:
```
django.db.models
```

---
  * target_content_type `ForeignKey` - The [content type](https://docs.djangoproject.com/en/3.0/ref/contrib/contenttypes/#the-contenttype-model) of the object being linked.
  * target_object_id `PositiveIntegerField` - The unique identification of the object.
  * target_content_object `GenericForeignKey` - The actual foreign key reference to another model.
