# -*- coding: utf-8 -*-
"""
Tests ContentType viewsets.
"""
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.base import TestBase

from tasking.tools import get_allowed_contenttypes
from tasking.viewsets import ContentTypeViewSet


class TestContentTypeViewSet(TestBase):
    """
    Test LocationViewSet class.
    """

    def setUp(self):
        super(TestContentTypeViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def test_list_contenttype(self):
        """
        Test that we can get the list of allowed content types
        """
        user = mommy.make('auth.User')
        view = ContentTypeViewSet.as_view({'get': 'list'})

        request = self.factory.get('/contenttypes')
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), get_allowed_contenttypes().count())
        self.assertTrue(
            ContentType.objects.filter(pk=response.data[1]['id']).exists())
