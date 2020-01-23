# Ona Tasking

[![Build Status](https://travis-ci.org/onaio/tasking.svg?branch=master)](https://travis-ci.org/onaio/tasking)

Ona-tasking is a Django application that allows users to implement tasking.

_We define tasking as an activity where you assign tasks to users, who then make submissions._

Full documentation [here](https://github.com/onaio/tasking/tree/master/docs).

## Requirements

- Python: 3.6, 3.7, 3.8
- Django: 2.2, 3.0

*Optional:* Ona-tasking was tested with [PostGIS](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/postgis/) as the database backend. We recommend that you utilize PostGIS.

## Installation

Install using pipenv:

```sh
$ pipenv install -e git+https://github.com/onaio/tasking.git#egg=ona-tasking
```

Optionally, you can install a specific tag or branch like this:

```sh
pipenv install -e git+https://github.com/onaio/tasking.git@<tag_number OR branch_name>#egg=ona-tasking
```

Then add the following to your `INSTALLED_APPS`:

```
[
...
# Third Party Packages required by ona-tasking
'django_countries',
'django_filters',
'mptt',
'rest_framework',
'rest_framework_gis',
# ona-tasking
'tasking.apps.TaskingConfig',
]
```

## Usage

Ona-tasking provides a good base for implementing tasking into your project. Here is a small example on how this can be done.

```python
...
from tasking.models import BaseTask


# Custom Task Model for application
class TodoTask(BaseTask):
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    class Meta:
        abstract = False

...

def create_task(request):
    assignee = request.POST['assignee']
    task = TodoTask.objects.create(
        assignee=assignee,
        creator=request.user,
        name='Fetch milk',
        description='Please buy 30 litres of milk and deliver them to my house',
        start=datetime.now()
    )
    return redirect('task_detail', task_id=task)
```

The example above depicts a small part of the available models and API in the package. Read more about what's provided by the package in our [docs](https://github.com/onaio/tasking/tree/master/docs).

## Contributing

Contributions are wholeheartedly welcome. Please have a look at our [contribution guidelines](https://github.com/onaio/tasking/blob/master/CONTRIBUTING.md) before contributing.
