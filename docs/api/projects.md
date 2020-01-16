# Projects

Adds ability to create, list, update, delete and retrieve Projects.

Once a Project is created it's stored in the database and can be retrieved via the API described below.

## API Endpoints

### POST /api/v1/projects

Creates a new project, requires a `name` , `target_content_type` and `target_id`.

```console
curl -X POST -H "Content-Type:application/json" -d '{"name": "Example Project", "target_content_type": 9, "target_id": "3"}' https://example.com/api/v1/projects
```

`name`: *string*.

`target_content_type`: *integer*, is a unique identifier for any of the allowed content types.

`target_id`: *integer*, is the target identifier.

It can also take additional inputs such as:

- `tasks`: *list of integers*, are the unique identifiers of Tasks.

### GET /api/v1/projects

Returns a list of all Projects.

```console
curl -X GET https://example.com/api/v1/projects
```

Returns a list of projects with specific a task if given `tasks` query parameter. The `tasks` query parameter takes a *list of integers* which are the unique identifiers of Tasks.

```console
curl -X GET https://example.com/api/v1/projects?tasks=1
```

Returns a list of all projects with a specific name if given `search` query parameter. The `search` query parameter takes a *string* which is the projects name.

```console
curl -X GET https://example.com/api/v1/projects?search=exampleproject
```

Returns a list of project ordered by name or creation date if given `ordering` query parameter. The `ordering` can be done in ascending order using either `name` or `created` and can be done in descending order using either `-name` or `-created`

```console
curl -X GET https://example.com/api/v1/projects?ordering=name,-created
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

Partially Updates a specific project with matching pk. Takes the same input as the POST create a project request with an additional project `id` in the url.

```console
curl -X PATCH -H "Content-Type:application/json" -d '{"name": "Eldorado Initiative"}' https://example.com/api/v1/projects/17
```
