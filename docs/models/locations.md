# Locations

Model to save real wold places. 

## BaseLocation

We need at least one of geopoint, radius or shapefile

Inherits:
```
mptt.models.MPTTModel
tasking.models.base.GeoTimeStampedModel
django.contrib.gis.db.Model
```

---
  * parent `TreeForeignKey` - A real world place that contains the current one. e.g a town is in a county
  * name `CharField` - _required_ name of the place
  * country `CountryField` - The country that the location is in
  * geopoint `PointField` - Geographical Point of the Location
  * radius `DecimalField` - radius from the geopoint
  * shapefile `PolygonField` - a [https://en.wikipedia.org/wiki/Shapefile](https://en.wikipedia.org/wiki/Shapefile) of the location


## Location
Concrete model for location. Implements BaseLocation as is.  
Inherits:
```
BaseLocation
```
