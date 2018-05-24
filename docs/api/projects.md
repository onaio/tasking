# Projects

Adds ability to create, list, update, delete and retrieve Projects.

Once a Project is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### POST /api/v1/projects

Creates a new project, requires a `name` , `target_content_type` and `target_id`. The `target_content_type` can be any of the allowed content types and `target_id` is the target identifier.

```console
curl -X POST -H "Content-Type:application/json" -d '{"name": "Example Project", "target_content_type": "task", "target_id": "3"}' https://example.com/api/v1/projects
```

### GET /api/v1/projects

Returns a list of all Projects.

```console
curl -X GET https://example.com/api/v1/projects
```

Returns a list of projects with specific a task if given `tasks` query parameter. The `tasks` is the target identifier.

```console
curl -X GET https://example.com/api/v1/projects?tasks=1
```

Returns a list of all projects with a specific name if given `search` query parameter.

```console
curl -X GET https://example.com/api/v1/projects?search=exampleproject
```

Returns a list of project ordered by name or creation date if given `ordering` query parameter. The `ordering` can be done using either `name` or `created`.

```console
curl -X GET https://example.com/api/v1/projects?ordering=name,created
```

### GET /api/v1/projects/[pk]

Returns a specific project with matching pk.

```console
curl -X GET https://example.com/api/v1/projects/18
```

This request will return a response containing the specific project.

```json
{
    "id": 18,
    "name": "Livestock prices",
    "tasks": [30, 31],
    "created": "2018-05-23T12:37:01.252225+03:00",
    "modified": "2018-05-23T12:37:01.252243+03:00",
    "target_content_type": 9,
    "target_id": 29
}
```

### DELETE /api/v1/projects/[pk]

Deletes a specific project with matching pk.

```console
curl -X DELETE https://example.com/api/v1/projects/17
```

### PATCH /api/v1/projects/[pk]

Partially Updates a specific project with matching pk.

```console
curl -X PATCH -H "Content-Type:application/json" -d '{"name": "Eldorado Initiative"}' https://example.com/api/v1/projects/17
```
