"""
Main init file for tasking app
"""

VERSION = (0, 3, 0)
__version__ = ".".join(str(v) for v in VERSION)
# pylint: disable=invalid-name
default_app_config = "tasking.apps.TaskingConfig"  # noqa
