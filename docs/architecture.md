# Architecture

ona-tasking is a Django app that adds `tasking` ([what is tasking?](https://github.com/onaio/tasking#what-is-tasking)) functionality to your project.

The functionality is provided via:

## 1. Models

ona-tasking includes a number of models that are useful for tasking.

### Task Model

This model represents an actual task.

### TaskSubmission Model

This model represents a task submissions.

### Location Model

This model represents a location in which a task can be performed.

### Project Model

This model represents a `project`, which is a way to group similar tasks.

### SegmentRule Model

The SegmentRule model is used to store rules that can be used to filter other
models.  ona-tasking uses it to filter tasks by certain user-defined criteria.

---

Each of the models above is implemented as an [abstract base model class](https://docs.djangoproject.com/en/2.0/topics/db/models/#abstract-base-classes) that can be
imported and extended by your own project.

Additionally, ona-tasking includes concrete models that extend the abstract
base classes.  These may be used straight out of the box if your project does
not require any modification of the base model classes.

## 2. API

TODO

## 3. Helper Functions

TODO
