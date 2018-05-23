# Segment Rules

Adds ability to create, list, update, delete and retrieve Segment Rules.

Once a Segment Rule is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### POST /api/v1/segment-rules

Creates a new segment rule, requires a `name`, `active` `target_content_type`, `target_field` and `target_field_value`. The `target_content_type` can be any of the allowed content types, `target_field` is a valid field of defined `target_content_type`, `active` has either true or false and `target_field_value` is desired value for `target_field`.

```console
curl -X POST -H "Content-Type:application/json" -d '{"name": "Rule Zero", "target_content_type": "task", "target_field": "id", "target_field_value": "6", "active": true}' https://example.com/api/v1/segment-rules
```

### GET /api/v1/segment-rules

Returns a list of all segment rules.

```console
curl -X GET https://example.com/api/v1/segment-rules
```

### GET /api/v1/segment-rules/[pk]

Returns a specific segment rule with maching pk.

```console
curl -X GET https://example.com/api/v1/segment-rules/45
```

This request returns a response containing the specific segment rule.

```json
{
    "description": "Some description",
    "active": true,
    "target_content_type": 9,
    "target_field": "id",
    "target_field_value": "6",
    "id": 45,
    "created": "2018-05-23T16:14:02.328128+03:00",
    "modified": "2018-05-23T16:14:02.328153+03:00",
    "name": "Rule Zero"
}

```

### DELETE /api/v1/segment-rules/[pk]

Deletes a specififc segment rule with matching pk.

```console
curl -X DELETE https://example.com/api/v1/segment-rules/45
```

### PATCH /api/v1/segment-rules/[pk]

Partially Updates a specific segment rule with matching pk.

```console
curl -X PATCH -H "Content-Type:application/json" -d '{"name": "Beta Rule"}' https://example.com/api/v1/segment-rules/17
```
