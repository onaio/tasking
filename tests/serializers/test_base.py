# -*- coding: utf-8 -*-
"""
base Serializer tes classes
"""
from __future__ import unicode_literals

from django.test import TestCase

from tasking.tools import get_allowed_contenttypes


class TestSerializerBase(TestCase):
    """
    Serializer base test class
    """

    def setUp(self):
        """
        Setup tests
        """

        self.task_type = get_allowed_contenttypes().filter(
            model='task').first()
