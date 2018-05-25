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
  * name `CharField` - name of the place
  * country `CountryField` - 
  * geopoint `PointField` - 
  * radius `DecimalField` - 
  * shapefile `PolygonField`


## Location
Concrete model for location. Implements BaseLocation as is.  
Inherits:
```
BaseLocation
```
