# Segment Rules

Adds ability to create, list, update, delete and retrieve Segment Rules.

Once a Segment Rule is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### GET /api/v1/segment-rules

Creates a new segment rule, requires a `name`, `target_content_type`, `target_field` and `target_field_value`. The `target_content_type` can be any of the allowed content types, `target_field` is a valid field of defined `target_content_type` and `target_field_value` is desired value for `target_field`.

```console
curl -X POST -H "Content-Type:application/json" -d '{"name": "Rule Zero", "description": "Some description", "target_content_type": "task", "target_field": "id", "target_field_value": "6", "active": true}' https://example.com/api/v1/segment-rules
```
