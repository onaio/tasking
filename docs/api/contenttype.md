# Content Type

Adds ability to list supported content types and their primary keys.

## API Endpoints

### GET /api/v1/contenttypes

Returns a list of all allowed content types and their identifiers.

```console
curl -X GET https://example.com/api/v1/contenttypes
```

This request will return a response containing the list of allowed content types.

```json
[
    {
        "id": 5,
        "app_label": "tasking",
        "model": "location"
    },
    {
        "id": 6,
        "app_label": "tasking",
        "model": "project"
    }
]
```
