# Locations

Adds ability to create, list, update, delete and retrieve Locations.

Once a Location is created it's stored in the database and can be retrieved from the API as shown below.

## API Endpoints

### POST /api/v1/locations

Creates a new location, requires a `name`.

```console
curl -x POST -H "Content-Type:application/json" -d '{"name": "HappyLand"}' https://example.com/api/v1/locations
```

### GET /api/v1/locations

Returns a list of all locations

```console
curl -X GET https://example.com/api/v1/locations
```

Returns a list of all locations with a specific parent location if given a `parent` query parameter. The `parent` is the target identifier for the parent location.

```console
curl -X GET https://example.com/api/v1/locations?parent=2
```

Returns a list of all locations in a specific country if given a `country` query parameter. The `country` is the Country Code for a Country

```console
curl -X GET https://example.com/api/v1/locations?country=KE
```

Returns a list of all locations with a specific name if given `search` query parameter.

```console
curl -X GET https://example.com/api/v1/locations?search=eldorado
```

Returns a list of locations ordered by name or creation date if given `ordering` query parameter. The `ordering` can be done using either `name` or `created`.

```console
curl -X GET https://example.com/api/v1/locations?ordering=name,created
```

### GET /api/v1/locations/[pk]

Returns a specific location with matching pk.

```console
curl -X GET https://example.com/api/v1/locations/24
```

This request will return a response containing the specific location.

```json
{
    "id": 24,
    "name": "Nairobi",
    "country": "KE",
    "geopoint": None,
    "radius": None,
    "shapefile": None,
    "parent": None,
    "created": "2018-05-23T14:48:42.169129+03:00",
    "modified": "2018-05-23T14:48:42.169151+03:00"
}
```

### DELETE /api/v1/locations/pk

Deletes a specific location with matching pk.

```console
curl -X DELETE https://example.com/api/v1/locations/23
```

### PATCH /api/v1/locations/[pk]

Partially Updates a specific location with matching pk.

```console
curl -X PATCH -H "Content-Type:application/json" -d '{"name": "Hyperion"}' https://example.com/api/v1/locations/24
```
