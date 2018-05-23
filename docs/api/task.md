# Tasks

Adds ability to create, list, update, delete and retrieve Tasks.

Once a Task is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### POST /api/v1/tasks

Creates a Task, requires a `name`, `timing_rule`, `target_content_type`, `target_id`. The `target_content_type` can be any of the allowed content types, `timing_rule` is an rrule and `target_id` is the target identifier.

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

Returns a list of all tasks with specific status if given `status` query parameter. The `status` is either ACTIVE, DEACTIVATED, EXPIRED or DRAFT

```console
curl -X GET https://example.com/api/v1/tasks?status=ACTIVE
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

### GET /api/v1/tasks
