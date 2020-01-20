"""
Apps module for tasking app
"""
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class TaskingConfig(AppConfig):
    """
    Tasking App Config Class
    """

    name = "tasking"
    app_label = "tasking"
    verbose_name = _("Tasking")

    def ready(self):
        """
        Do stuff when the app is ready
        """
        # set up app settings
        # pylint: disable=import-outside-toplevel
        from django.conf import settings
        import tasking.settings as defaults

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
