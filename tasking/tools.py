# -*- coding: utf-8 -*-
"""
Tools for tasking
"""
from __future__ import unicode_literals
import operator
from functools import reduce

from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

DEFAULT_ALLOWED_CONTENTTYPES = [
    {'app_label': 'tasking', 'model': 'task'},
    {'app_label': 'tasking', 'model': 'location'},
    {'app_label': 'tasking', 'model': 'project'},
    {'app_label': 'tasking', 'model': 'segmentrule'},
    {'app_label': 'tasking', 'model': 'submission'},
    {'app_label': 'auth', 'model': 'user'},
    {'app_label': 'auth', 'model': 'group'},
    {'app_label': 'logger', 'model': 'xform'},
    {'app_label': 'logger', 'model': 'instance'},
    {'app_label': 'logger', 'model': 'project'}
]

ALLOWED_CONTENTTYPES = getattr(settings, 'TASKING_ALLOWED_CONTENTTYPES',
                               DEFAULT_ALLOWED_CONTENTTYPES)


def get_allowed_contenttypes(allowed_content_types=ALLOWED_CONTENTTYPES):
    """
    Returns a queryset of allowed content_types
    """
    filters = [Q(app_label=item['app_label'], model=item['model']) for item in
               allowed_content_types]
    if filters:
        return ContentType.objects.filter(reduce(operator.or_, filters))
    return ContentType.objects.none()
