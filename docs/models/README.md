# Tasking models



### GeoTimeStampedModel
Though it may seem redundant [GeoDjango model API](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/model-api/) re-exports [DateTimeField](https://docs.djangoproject.com/en/2.0/ref/models/fields/#datetimefield) from django models but we still create a [GeoTimeStampedModel](./base.md#geotimestampedmodel) so that inheriting classes can inherit other GeoDjango model fields and APIs.
