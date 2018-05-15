# -*- coding: utf-8 -*-
"""
Tests SegmentRule viewsets.
"""
from __future__ import unicode_literals

from django.utils import six

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.base import TestBase

from tasking.models import SegmentRule
from tasking.viewsets import SegmentRuleViewSet


class TestSegmentRuleViewSet(TestBase):
    """
    Test SegmentRuleViewSet class.
    """

    def setUp(self):
        super(TestSegmentRuleViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_segment_rule(self):
        """
        Helper to create a single segment rule
        """
        user = mommy.make('auth.User')

        data = {
            'name': 'Rule Zero',
            'description': 'Some description',
            'target_content_type': self.task_type.id,
            'target_field': 'id',
            'target_field_value': '6',
            'active': True
        }

        view = SegmentRuleViewSet.as_view({'post': 'create'})
        request = self.factory.post('/segment-rule', data)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertDictContainsSubset(data, response.data)
        return response.data

    def test_create_segment_rule(self):
        """
        Test POST /segment-rules adding a new segment rule.
        """
        self._create_segment_rule()

    def test_create_with_bad_data(self):
        """
        Test that we get appropriate errors when trying to create an object
        with bad data
        """
        alice_user = mommy.make('auth.User')

        # test bad content type validation
        bad_content_type = {
            'name': 'Rule Zero',
            'description': 'Some description',
            'target_content_type': 999,
            'target_field': 'id',
            'target_field_value': '6',
            'active': True
        }

        view = SegmentRuleViewSet.as_view({'post': 'create'})
        request = self.factory.post('/segment-rule', bad_content_type)
        # Need authenticated user
        force_authenticate(request, user=alice_user)
        response = view(request=request)

        self.assertEqual(response.status_code, 400)

        self.assertIn('target_content_type', response.data.keys())
        self.assertEqual(
            'Invalid pk "999" - object does not exist.',
            six.text_type(response.data['target_content_type'][0]))

    def test_delete_segment_rule(self):
        """
        Test DELETE tasks.
        """
        user = mommy.make('auth.User')
        segment_rule = mommy.make('tasking.SegmentRule')

        # assert that segment rule exists
        # pylint: disable=no-member
        self.assertTrue(SegmentRule.objects.filter(
            pk=segment_rule.id).exists())
        # delete segment rule
        view = SegmentRuleViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(
            '/segment-rule/{id}'.format(id=segment_rule.id))
        force_authenticate(request, user=user)
        response = view(request=request, pk=segment_rule.id)
        # assert that segment rule was deleted
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            SegmentRule.objects.filter(pk=segment_rule.id).exists())

    def test_retrieve_segment_rule(self):
        """
        Test GET /segment-rule/[pk] return a segment rule matching pk.
        """
        user = mommy.make('auth.User')
        segment_rule_data = self._create_segment_rule()
        view = SegmentRuleViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            '/segment-rule/{id}'.format(id=segment_rule_data['id']))
        force_authenticate(request, user=user)
        response = view(request=request, pk=segment_rule_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, segment_rule_data)

    def test_list_segment_rules(self):
        """
        Test GET /segment-rule listing of segment rules for specific forms.
        """
        user = mommy.make('auth.User')
        segment_rule_data = self._create_segment_rule()
        view = SegmentRuleViewSet.as_view({'get': 'list'})

        request = self.factory.get('/segment-rule')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data.pop(), segment_rule_data)

    def test_update_segment_rule(self):
        """
        Test UPDATE segement rule
        """
        user = mommy.make('auth.User')
        segment_rule_data = self._create_segment_rule()

        data = {
            'name': 'Rule One',
            'description': 'i love oov',
            'target_field_value': 'mosh',
            'active': False,
            'target_field': 'username',
            'target_content_type': self.user_type.id
        }

        view = SegmentRuleViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            '/segment-rule/{id}'.format(id=segment_rule_data['id']), data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=segment_rule_data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual('Rule One', response.data['name'])
        self.assertEqual('i love oov', response.data['description'])
        self.assertEqual('mosh', response.data['target_field_value'])
        self.assertFalse(response.data['active'])
        self.assertEqual('username', response.data['target_field'])
        self.assertEqual(
            self.user_type.id, response.data['target_content_type'])

    # pylint: disable=too-many-locals
    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        segment_rule_data = self._create_segment_rule()
        segment_rule = mommy.make('tasking.SegmentRule')

        # test that you need authentication for creating a segment rule
        good_data = {
            'name': 'Rule Zero',
            'description': 'Some description',
            'target_content_type': self.task_type.id,
            'target_field': 'id',
            'target_field_value': '6',
            'active': True
        }
        view = SegmentRuleViewSet.as_view({'post': 'create'})
        request = self.factory.post('/segment-rule', good_data)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response.data['detail']))

        # test that you need authentication for retrieving a segment rule
        view2 = SegmentRuleViewSet.as_view({'get': 'retrieve'})
        request2 = self.factory.get(
            '/segment-rule/{id}'.format(id=segment_rule_data['id']))
        response2 = view2(request=request2, pk=segment_rule_data['id'])
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response2.data['detail']))

        # test that you need authentication for listing a segment rule
        view3 = SegmentRuleViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/segment-rule')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response3.data['detail']))

        # test that you need authentication for deleting a segment rule
        # pylint: disable=no-member
        self.assertTrue(
            SegmentRule.objects.filter(pk=segment_rule.id).exists())

        view4 = SegmentRuleViewSet.as_view({'delete': 'destroy'})
        request4 = self.factory.delete(
            '/segment-rule/{id}'.format(id=segment_rule.id))
        response4 = view4(request=request4, pk=segment_rule.id)

        self.assertEqual(response4.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response4.data['detail']))

        # test that you need authentication for updating a segment rule
        data = {
            'name': 'Rule Zero Plus',
        }
        view5 = SegmentRuleViewSet.as_view({'patch': 'partial_update'})
        request5 = self.factory.patch(
            '/segment-rule/{id}'.format(id=segment_rule_data['id']), data=data)
        response5 = view5(request=request5, pk=segment_rule_data['id'])

        self.assertEqual(response5.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            six.text_type(response5.data['detail']))
