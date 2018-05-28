# Occurences

A read only endpoint that gives **when** a task is taking place.

## API Endpoints

### GET /api/v1/occurences/[pk]

```console
curl https://example.com/api/v1/occurences/24
```

This request returns a response containing a specific task occurence.

```json
{
    "id": 24,
    "task": 1,
    "date": "2018-05-23T14:48:42.169151+03:00",
    "start_time": "2018-05-24T07:00:00.169151+03:00",
    "end_time": "2018-05-23T14:30:00.169151+03:00",
    "time_string": "24th May 2018, 7 a.m. to 2:30 p.m.",
    "created": "2018-05-23T14:48:42.169129+03:00",
    "modified": "2018-05-23T14:48:42.169151+03:00"
}

```
