# Location

Model used to represent real world locations.

## BaseLocation

Abstract class implementing locations.

Because locations are hierarchical in nature we use pre-ordered tree traversal to store location model objects.
These allow for faster reads/retrieval but the trade of being slower writes and modification.
We use [django-mptt](https://github.com/django-mptt/django-mptt) which has Modified Preorder Tree Traversal support to achieve this.

Inherits:
```
mptt.models.MPTTModel
tasking.models.base.GeoTimeStampedModel
django.contrib.gis.db.Model
```

---
  * parent `TreeForeignKey` - A real world place that contains the current one. e.g a town is in a county.
  * name `CharField` - _required_ Name of the location.
  * description `TextField` - Description of location.
  * country `CountryField` - The country that the location is in.
  * geopoint `PointField` - Geographical point of the Location.
  * radius `DecimalField` - Radius from the geopoint.
  * shapefile `PolygonField` - A [shapefile](https://en.wikipedia.org/wiki/Shapefile) of the location.


## Location

Concrete class implementing locations.

Inherits:
```
BaseLocation
```

---
  * location_type `ForeignKey` - A way to categorize locations. e.g Markets, Restaurants etc.
