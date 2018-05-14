# Installation

## Official releases

None yet.

## Development version

You can get the source code from our [git](https://git-scm.com/) repository.

```sh

git clone https://github.com/onaio/tasking.git

```

Add the resulting folder to your [PYTHONPATH](http://docs.python.org/tut/node8.html#SECTION008110000000000000000) or symlink the `tasking` directory inside it into a directory which is on your PYTHONPATH, such as your Python installation’s site-packages directory.

You can verify that the application is available on your PYTHONPATH by opening a Python interpreter and entering the following commands:

```sh

python manage.py shell

>>> import tasking

>>> tasking.VERSION

(0, 0, 1)

```

When you want to update your copy of the source code, run git pull from within the tasking directory.

### Caution
    Please note that the development version may contain bugs which are not present in the release version and may introduce backwards-incompatible changes.
