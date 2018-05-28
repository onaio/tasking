# ona-tasking

[![Build Status](https://travis-ci.org/onaio/tasking.svg?branch=master)](https://travis-ci.org/onaio/tasking)

A Django app that provides adds tasking to your Django project.

**Table of Contents**

* [Design guidelines](https://github.com/onaio/tasking/blob/master/docs/design.md)
* [Installation](https://github.com/onaio/tasking/blob/master/docs/installation.md)
* [Architecture](https://github.com/onaio/tasking/blob/master/docs/architecture.md)
* [Usage](https://github.com/onaio/tasking/blob/master/docs/usage.md)
* [What is tasking?](https://github.com/onaio/tasking#what-is-tasking)
* [Testing](https://github.com/onaio/tasking#testing)

## What is tasking?

We define tasking as an activity where you assign tasks to users, who then make task submissions.

Some definitions:

### Task

A piece of work to be done or undertaken.

Tasks are usually very specific to one's own needs.  For instance, one task might be to fill in a form for a survey, while another may be to fix a broken car.

ona-tasking tries to implement tasks in an abstract and extensible way so that you can integrate them easily into your own project.

This is done by implementing:

* a concrete `Task` model class that has minimal tasking features that you can use right out of the box to represent a Task
* an abstract `BaseTask` model class that you can inherit and do with as you please
* utility functions to aid in tasking

### User

A person who does a task.

ona-tasking assumes that a user is a Django user - either an instance of the `django.contrib.auth.models.User` class, or your own `User` class.

### Task Submission

Once a user does a task, this is what they submit.  It can then be validated and verified to ascertain that it meets the requirements of the task.

Because tasks can be varied in how they actually work, task submissions can be very different depending on your particular use-case.  Similar to Tasks above, we have:

* a `Submission` model that you can use straight out of the box.  It only includes minimal features, however.
* an abstract `BaseSubmission` model class that you can inherit and extend

---

Therefore, ona-tasking gives you the ability to create tasks.  Users can do these tasks and then make submissions to you.  You can then approve/reject these task submissions.

## Testing

```sh

pip install -U tox

tox

```
