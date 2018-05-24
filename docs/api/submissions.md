# Submissions

Adds ability to create, list, update, delete and retrieve Submissions.

Once a Submission is created it's stored in the database and can be retrieved via the API described below.

## API Endpoint

### POST /api/v1/submissions

Creates a new submission, requires a `task` , `target_content_type`, `target_id`, `submission_time` and `user`.

```console
curl -X POST -H "Content-Type:application/json" -d '{"task": 25, "target_content_type": 9, "target_id": 147}' https://example.com/api/v1/submissions
```

`target_content_type`: *integer*, is a unique identifier for any of the allowed content types.

`task`: *integer*, is a unique identifier for a `Task` object.

`target_id`: *integer*, is the target identifier.

`submission_time`: *Date and Time*.

`user`: *integer*, is the unique identifier for the user.

It can take additional inputs in the content such as:

- `comments`: *string*.
- `approved`: *boolean*, on creation of submission defaults to False.
- `valid`: *boolean*, on creation of submission defaults to False.

### GET /api/v1/submissions

Returns a list of all submissions

```console
curl -X GET https://example.com/api/v1/submissions
```

Returns a list of submissions for a specific task name if given `search` query parameter. The `search` query parameter takes a *string* which is the tasks name.

```console
curl -X GET https://example.com/api/v1/projects?search=exampletask
```

Returns a list of submissions for a specific task if given `task` query parameter. The `task` query parameter takes a *integer* which is a unique identifier for a task.

```console
curl -X GET https://example.com/api/v1/submissions?task=4
```

Returns a list of submissions for a specific location if given `location` query parameter. The `location` query parameter takes a *integer* which is a unique identifier for a location.

```console
curl -X GET https://example.com/api/v1/submissions?location=46
```

Returns a list of submissions from a specific user if given `user` query parameter. The `user` query parameter takes a *integer* which is a unique identifier for a user.

```console
curl -X GET https://example.com/api/v1/submissions?user=17
```

Returns a list of all approved or disapproved submissions if given `approved` query parameter. The `aprroved` query parameter takes a *boolean*.

```console
curl -X GET https://example.com/api/v1/submissions?approved=1
```

Returns a list of all valid or invalid submissions if given `approved` query parameter. The `valid` query parameter takes a *boolean*.

```console
curl -X GET https://example.com/api/v1/submissions?valid=0
```

Returns a list of all submissions ordered by either creation date, valid status, approved status, time of submission or task if given `ordering` query parameter. The `ordering` can be done in ascending order using either `created`, `valid`, `approved`, `submission_time` or `task__id` and in descending order using either `-created`, `-valid`, `-approved`, `-submission_time` or `-task__id`

```console
curl -X GET https://example.com/api/v1/submissions?ordering=created,valid,submission_time,task__id,approved
```

### GET /api/v1/submissions/[pk]

Return a specific submission with matching pk.

```console
curl -X GET https://example.com/api/v1/submissions/20
```

This request will return a response containing the specific submission.

```json
{
    "id": 20,
    "modified": "2018-05-23T15:32:50.985721+03:00",
    "created": "2018-05-23T15:32:50.985704+03:00",
    "task": 177,
    "location": 55,
    "user": 196,
    "submission_time": "2018-05-23T15:32:50.974830+03:00",
    "valid": true,
    "approved": true,
    "comments": "Approved",
    "target_content_type": 3,
    "target_id": 195
}
```

### DELETE /api/v1/submissions/[pk]

Deletes a specific submission with matching pk.

```console
curl -X DELETE https://example.com/api/v1/submissions/90
```

### PATCH /api/v1/submissions/[pk]

Partially Updates a specific project with matching pk. Takes the same input as POST create submission request but with an additional submission `id` in the url.

```console
curl -X PATCH -H "Content-Type:application/json" -d '{"comments": "Bad Data"}' https://example.com/api/v1/submissions/17
```
