# Tasks

Adds ability to create, list, update, delete and retrieve Tasks.

Once a Task is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### POST /api/v1/tasks

Creates a Task, requires a `name`, `timing_rule`, `target_content_type` and `target_id`. The `target_content_type` can be any of the allowed content types, `timing_rule` is an rrule and `target_id` is the target identifier.

```console
curl -X POST -H "Content-Type:application/json" '{"name": "Cow price", "description": "Some description", "total_submission_target": 10, "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5", "target_content_type": "task", "target_id": 234}' https://example.com/api/v1/tasks
```

### GET /api/v1/tasks

Returns a list of all tasks.

```console
curl -X GET https://example.com/api/v1/tasks
```

Returns a list of all tasks with specific locations if given `locations` query parameter. The `locations` is a location(s) identifier.

```console
curl -X GET https://example.com/api/v1/tasks?locations=1
```

Returns a list of all tasks with specific status if given `status` query parameter. The `status` is either a, b, c or d

```console
curl -X GET https://example.com/api/v1/tasks?status=b
```

Returns a list of all tasks in a specific project if given `project` query parameter. The `project` is a project identifier.

```console
curl -X GET https://example.com/api/v1/tasks?project=498
```

Returns a list of all tasks with a specific parent if given `parent` query parameter.

```console
curl -X GET https://example.com/api/v1/tasks?parent=43
```

Returns a list of all tasks ordered by either creation date, task status or name of task if given a `ordering` query parameter. The `ordering` has either `created`, `status` or `name`.

```console
curl -X GET https://example.com/api/v1/projects?ordering=name,created,status
```

### GET /api/v1/tasks/[pk]

Returns a specific task with matching pk.

```console
curl -X GET https://example.com/api/v1/tasks/81
```

This request returns a response containing the specific task.

```json
{
    "id": 81,
    "created": "2018-05-24T09:00:06.750893+03:00",
    "modified": "2018-05-24T09:00:06.750912+03:00",
    "name": "Cow price",
    "parent": null,
    "description": "Some description",
    "start": "2018-05-24T09:00:06+03:00",
    "end": "2018-07-03T09:00:06+03:00",
    "timing_rule": "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5", "total_submission_target": 10,
    "user_submission_target": null,
    "status": "d",
    "target_content_type": 9,
    "target_id": 45,
    "segment_rules": [8, 7],
    "locations": []
}
```

### DELETE /api/v1/tasks/[pk]

Deletes a specific task with matching pk.

```console
curl -X DELETE https://example.com/api/v1/tasks/81
```

### PATCH /api/v1/tasks/[pk]

Partially updates a specific task with matching pk.

```console
curl -X PATCH "Content-Type:application/json" -d '{"name": "Cheese Shop Locations"}' https://example.com/api/v1/tasks/18
```
