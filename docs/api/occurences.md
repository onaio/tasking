# Occurences

A read only endpoint that gives **when** a task is taking place.

## API Endpoints

### GET /api/v1/occurences


You can filter by fields:
 - task
 - date
 - start_time
 - end_time

time lookups:
 - exact
 - gt
 - lt
 - lte
 - gte

datetime lookups:
 - exact
 - gt
 - lt
 - gte
 - lte
 - year
 - year__gt
 - year__lt
 - year__gte
 - year__lte
 - month
 - month__gt
 - month__lt
 - month__gte
 - month__lte
 - day day__gt
 - day__lt
 - day__gte
 - day__lte


#### Filter by task

```console
curl https://example.com/api/v1/occurrences?task=24
```

This request returns a response containing a specific task occurrence.

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

#### Filter by start time

```console
curl https://example.com/api/v1/occurrences?start_time__gte=17:00:00
```

```json
[
    {
        "id": 24,
        "task": 1,
        "date": "2018-05-23T14:48:42.169151+03:00",
        "start_time": "2018-05-24T17:00:00.169151+03:00",
        "end_time": "2018-05-23T23:30:00.169151+03:00",
        "time_string": "24th May 2018, 7 a.m. to 2:30 p.m.",
        "created": "2018-05-23T14:48:42.169129+03:00",
        "modified": "2018-05-23T14:48:42.169151+03:00"
    },
    {
        "id": 24,
        "task": 1,
        "date": "2018-05-23T14:48:42.169151+03:00",
        "start_time": "2018-05-24T19:00:00.169151+03:00",
        "end_time": "2018-05-23T19:30:00.169151+03:00",
        "time_string": "24th May 2018, 7 a.m. to 2:30 p.m.",
        "created": "2018-05-23T14:48:42.169129+03:00",
        "modified": "2018-05-23T14:48:42.169151+03:00"
    },
    {
        "id": 24,
        "task": 1,
        "date": "2018-05-23T14:48:42.169151+03:00",
        "start_time": "2018-05-24T20:00:00.169151+03:00",
        "end_time": "2018-05-23T23:30:00.169151+03:00",
        "time_string": "24th May 2018, 7 a.m. to 2:30 p.m.",
        "created": "2018-05-23T14:48:42.169129+03:00",
        "modified": "2018-05-23T14:48:42.169151+03:00"
    }
]
```


#### Filter by date

```console
curl https://example.com/api/v1/occurrences?date__year__gte=2017
```

```json
[
    {
        "id": 24,
        "task": 1,
        "date": "2018-05-23T14:48:42.169151+03:00",
        "start_time": "2018-05-24T07:00:00.169151+03:00",
        "end_time": "2017-05-23T14:30:00.169151+03:00",
        "time_string": "24th May 2018, 7 a.m. to 2:30 p.m.",
        "created": "2017-05-23T14:48:42.169129+03:00",
        "modified": "2017-05-23T14:48:42.169151+03:00"
    },
    {
        "id": 25,
        "task": 1,
        "date": "2018-05-23T14:48:42.169151+03:00",
        "start_time": "2018-05-24T07:00:00.169151+03:00",
        "end_time": "2017-05-23T14:30:00.169151+03:00",
        "time_string": "24th May 2018, 7 a.m. to 2:30 p.m.",
        "created": "2018-05-23T14:48:42.169129+03:00",
        "modified": "2017-05-23T14:48:42.169151+03:00"
    },
    {
        "id": 27,
        "task": 1,
        "date": "2018-05-23T14:48:42.169151+03:00",
        "start_time": "2018-05-24T07:00:00.169151+03:00",
        "end_time": "2018-05-23T14:30:00.169151+03:00",
        "time_string": "24th May 2018, 7 a.m. to 2:30 p.m.",
        "created": "2018-05-23T14:48:42.169129+03:00",
        "modified": "2017-05-23T14:48:42.169151+03:00"
    }
]
```
