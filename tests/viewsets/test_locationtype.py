"""
Tests Project viewsets.
"""
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate

from tasking.models import LocationType
from tasking.viewsets import LocationTypeViewSet


class TestLocationTypeViewSet(TestCase):
    """
    Test LocationTypeViewset class.
    """

    def setUp(self):
        super(TestLocationTypeViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_location_type(self):
        """
        Helper to create a single location type
        """

        user = mommy.make('auth.User')

        data = {
            'name': "Market",
        }

        view = LocationTypeViewSet.as_view({'post': 'create'})
        request = self.factory.post('/locationtypes', data)
        # Need authenticated user
        force_authenticate(request, user=user)
        response = view(request=request)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertDictContainsSubset(data, response.data)
        return response.data

    def test_create_location_type(self):
        """
        Test POST /locationtypes adding a new project.
        """
        self._create_location_type()

    def test_delete_location_type(self):
        """
        Test DELETE locationtype.
        """
        user = mommy.make('auth.User')
        locationtype = mommy.make('tasking.LocationType')

        # pylint: disable=no-member
        self.assertTrue(
            LocationType.objects.filter(pk=locationtype.id).exists())

        view = LocationTypeViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(
            f'/locationtypes/{locationtype.id}')
        force_authenticate(request, user=user)
        response = view(request=request, pk=locationtype.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            LocationType.objects.filter(pk=locationtype.id).exists())

    def test_retrieve_location_type(self):
        """
        Test GET /locationtypes/[pk] return a project matching pk.
        """
        user = mommy.make('auth.User')
        locationtype_data = self._create_location_type()
        locationtype_id = locationtype_data['id']

        view = LocationTypeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            f'/locationtypes/{locationtype_id}')
        force_authenticate(request, user=user)
        response = view(request=request, pk=locationtype_id)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, locationtype_data)

    def test_list_location_type(self):
        """
        Test GET /locationtypes listing of locationtypes
        """
        user = mommy.make('auth.User')
        locationtype_data = self._create_location_type()
        view = LocationTypeViewSet.as_view({'get': 'list'})

        request = self.factory.get('/locationtypes')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data.pop(), locationtype_data)

    def test_update_location_type(self):
        """
        Test UPDATE locationtype
        """
        user = mommy.make('auth.User')
        locationtype_data = self._create_location_type()
        locationtype_id = locationtype_data['id']

        data = {
            'name': "Hospital",
            }

        view = LocationTypeViewSet.as_view({'patch': 'partial_update'})
        request = self.factory.patch(
            f'/locationtypes/{locationtype_id}', data=data)
        force_authenticate(request, user=user)
        response = view(request=request, pk=locationtype_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('Hospital', response.data['name'])

    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        locationtype_data = self._create_location_type()
        locationtype_id = locationtype_data['id']
        locationtype = mommy.make('tasking.LocationType')

        # test that you need authentication for creating a locationtype
        good_data = {
            'name': "Household",
        }
        view = LocationTypeViewSet.as_view({'post': 'create'})
        request = self.factory.post('/locationtypes', good_data)
        response = view(request=request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response.data['detail']))

        # test that you need authentication for retrieving a locationtype
        view2 = LocationTypeViewSet.as_view({'get': 'retrieve'})
        request2 = self.factory.get(
            f'/locationtypes/{locationtype_id}')
        response2 = view2(request=request2, pk=locationtype_id)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response2.data['detail']))

        # test that you need authentication for listing locationtype
        view3 = LocationTypeViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/locationtypes')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response3.data['detail']))

        # test that you need authentication for deleting a locationtype
        # pylint: disable=no-member
        self.assertTrue(
            LocationType.objects.filter(pk=locationtype.id).exists())

        view4 = LocationTypeViewSet.as_view({'delete': 'destroy'})
        request4 = self.factory.delete(
            f'/locationtypes/{locationtype.id}')
        response4 = view4(request=request4, pk=locationtype.id)

        self.assertEqual(response4.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response4.data['detail']))

        # test that you need authentication for updating a locationtype
        data = {
            'name': "Landfill",
            }

        view5 = LocationTypeViewSet.as_view({'patch': 'partial_update'})
        request5 = self.factory.patch(
            f'/locationtypes/{locationtype_id}', data=data)
        response5 = view5(request=request5, pk=locationtype_id)

        self.assertEqual(response5.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response5.data['detail']))
