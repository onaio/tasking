# Documentation

Ona Tasking provides tasking functionality via:

* [Models](https://github.com/onaio/tasking/tree/master/docs/models):
    * Abstract model classes : These are classes that can be imported and extended by your own project. The classes provided the most basic requirements of a task. _You can read more about Django abstract base classes [here](https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes)._

    * Concrete model classes: These are classes that extend our base classes. They can be used out of the box if your project does not require any modification of the base model classes.

* [APIs](https://github.com/onaio/tasking/tree/master/docs/models): These API endpoints expose the models using [DRF](http://www.django-rest-framework.org/).
