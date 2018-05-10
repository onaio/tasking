# -*- coding: utf-8 -*-
"""
Test for SegmentRuleSerializer
"""
from __future__ import unicode_literals

from collections import OrderedDict

from django.test import TestCase
from django.utils import six, timezone

from model_mommy import mommy
from rest_framework.exceptions import ValidationError

from tasking.common_tags import TARGET_DOES_NOT_EXIST
from tasking.serializers import SegmentRuleSerializer
from tasking.utils import get_target


class TestSegmentRuleSerializer(TestCase):
    """
    Test the SegmentRuleSerializer
    """
