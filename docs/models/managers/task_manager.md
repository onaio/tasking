# Task Manager

Custom manager for Task Model.

## Methods

`get_queryset`: Custom get_queryset method that adds a *submission_count* annotation.

- `submission_count`: Annotation that returns a count of all submissions linked to a task.
