"""
Tests TaskOccurrence viewsets.
"""
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from tests.base import TestBase

from tasking.models import TaskOccurrence
from tasking.serializers import TaskOccurrenceSerializer
from tasking.viewsets import TaskOccurrenceViewSet


class TestTaskOccurrenceViewSet(TestBase):
    """
    Test TaskOccurrenceViewSet class.
    """

    def setUp(self):
        super(TestTaskOccurrenceViewSet, self).setUp()
        self.factory = APIRequestFactory()

    def _create_occurrence(self):
        """
        Helper to create a single occurrence
        """
        task = mommy.make('tasking.Task', name='d12')

        data = {
            'task': task.id,
            'date': '2018-05-12',
            'start_time': '07:00',
            'end_time': '19:30',
        }

        serializer_instance = TaskOccurrenceSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        serializer_instance.save()

        return serializer_instance.data

    def test_retrieve_occurrence(self):
        """
        Test GET /occurrence/[pk] return a occurrence matching pk.
        """
        user = mommy.make('auth.User')
        occurrence_data = self._create_occurrence()
        occurrence_id = occurrence_data['id']
        view = TaskOccurrenceViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            f'/occurrence/{occurrence_id}')
        force_authenticate(request, user=user)
        response = view(request=request, pk=occurrence_id)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, occurrence_data)

    def test_list_occurrences(self):
        """
        Test GET /occurrence listing of occurrences for specific forms.
        """
        user = mommy.make('auth.User')
        occurrence_data = self._create_occurrence()
        view = TaskOccurrenceViewSet.as_view({'get': 'list'})

        request = self.factory.get('/occurrence')
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data.pop(), occurrence_data)

    def test_authentication_required(self):
        """
        Test that authentication is required for all viewset actions
        """
        occurrence_data = self._create_occurrence()
        occurrence_id = occurrence_data['id']

        # test that you need authentication for retrieving a occurrence
        view2 = TaskOccurrenceViewSet.as_view({'get': 'retrieve'})
        request2 = self.factory.get(
            f'/occurrence/{occurrence_id}')
        response2 = view2(request=request2, pk=occurrence_id)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response2.data['detail']))

        # test that you need authentication for listing a occurrence
        view3 = TaskOccurrenceViewSet.as_view({'get': 'list'})
        request3 = self.factory.get('/occurrence')
        response3 = view3(request=request3)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(
            'Authentication credentials were not provided.',
            str(response3.data['detail']))

    def test_task_filter(self):
        """
        Test that you can filter by task
        """
        user = mommy.make('auth.User')
        task = mommy.make('tasking.Task')

        # make a bunch of occurrences
        mommy.make('tasking.TaskOccurrence', _quantity=7)

        # make one occurrence using the task
        occurrence = mommy.make('tasking.TaskOccurrence', task=task)

        # check that we have 8 occurrences
        # pylint: disable=no-member
        self.assertEqual(TaskOccurrence.objects.all().count(), 8)

        view = TaskOccurrenceViewSet.as_view({'get': 'list'})

        # test that we get occurrences for our task
        request = self.factory.get('/occurrences', {'task': task.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], occurrence.id)

    def test_location_filter(self):
        """
        Test that you can filter by location
        """
        user = mommy.make('auth.User')
        location = mommy.make('tasking.Location')

        # make a bunch of occurrences
        mommy.make('tasking.TaskOccurrence', _quantity=7)

        # make one occurrence using the location
        occurrence = mommy.make('tasking.TaskOccurrence', location=location)

        # check that we have 8 occurrences
        # pylint: disable=no-member
        self.assertEqual(TaskOccurrence.objects.all().count(), 8)

        view = TaskOccurrenceViewSet.as_view({'get': 'list'})

        # test that we get occurrences for our location
        request = self.factory.get('/occurrences', {'location': location.id})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], occurrence.id)

    def test_date_filter(self):
        """
        Test that you can filter by date
        """
        user = mommy.make('auth.User')
        task = mommy.make('tasking.Task')

        # make a bunch of occurrences
        mommy.make('tasking.TaskOccurrence', _quantity=7, date='2018-07-12')

        # make one occurrence using a unique date
        occurrence = mommy.make(
            'tasking.TaskOccurrence', task=task, date='2017-09-09')

        # check that we have 8 occurrences
        # pylint: disable=no-member
        self.assertEqual(TaskOccurrence.objects.all().count(), 8)

        view = TaskOccurrenceViewSet.as_view({'get': 'list'})

        # test that we get occurrences for our unique
        request = self.factory.get('/occurrences', {'date': '2017-09-09'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], occurrence.id)

        # make some occurrences that happen after 2018-07-12
        mommy.make('tasking.TaskOccurrence', _quantity=5, date='2018-11-11')

        # test that we can get occurrences before or after a certain date
        request2 = self.factory.get('/occurrences', {'date__gt': '2018-07-13'})
        force_authenticate(request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 5)

        request3 = self.factory.get('/occurrences', {'date__lt': '2018-07-13'})
        force_authenticate(request3, user=user)
        response3 = view(request=request3)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 8)

    def test_start_time_filter(self):
        """
        Test that you can filter by start_time
        """
        user = mommy.make('auth.User')
        view = TaskOccurrenceViewSet.as_view({'get': 'list'})
        # make some poccurrences that start at 7
        mommy.make(
            'tasking.TaskOccurrence', _quantity=5, start_time='07:00')

        # make some occurrences that happen after 9:00
        mommy.make(
            'tasking.TaskOccurrence', _quantity=6, start_time='09:15')

        # test that we can get occurrences before or after a certain time
        request2 = self.factory.get(
            '/occurrences', {'start_time__gte': '09:15'})
        force_authenticate(request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 6)

        request3 = self.factory.get(
            '/occurrences', {'start_time__lt': '09:15'})
        force_authenticate(request3, user=user)
        response3 = view(request=request3)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 5)

    def test_end_time_filter(self):
        """
        Test that you can filter by end_time
        """
        user = mommy.make('auth.User')
        view = TaskOccurrenceViewSet.as_view({'get': 'list'})
        # make some poccurrences that end at 5pm
        mommy.make(
            'tasking.TaskOccurrence', _quantity=5, end_time='17:00')

        # make some occurrences that end after 9pm
        mommy.make(
            'tasking.TaskOccurrence', _quantity=6, end_time='21:15')

        # test that we can get occurrences before or after a certain time
        request2 = self.factory.get(
            '/occurrences', {'end_time__gte': '21:15'})
        force_authenticate(request2, user=user)
        response2 = view(request=request2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 6)

        request3 = self.factory.get(
            '/occurrences', {'end_time__lt': '21:15'})
        force_authenticate(request3, user=user)
        response3 = view(request=request3)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.data), 5)

    def test_occurrence_sorting(self):
        """
        Test that we can sort occurrences
        """
        user = mommy.make('auth.User')
        view = TaskOccurrenceViewSet.as_view({'get': 'list'})

        # make some occurrences that have different dates and start and end
        # times
        for i in range(1, 7):
            mommy.make(
                'tasking.TaskOccurrence',
                date=f'2018-05-0{i}',
                start_time=f'0{i}:00',
                end_time=f'{i + 10}:00'
            )

        # test sorting by date ascending
        request = self.factory.get(
            '/occurrences', {'ordering': 'date'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        # pylint: disable=no-member
        self.assertEqual(len(response.data), TaskOccurrence.objects.count())
        self.assertEqual('2018-05-01', response.data[0]['date'])
        self.assertEqual('2018-05-06', response.data[-1]['date'])

        # test sorting by start_time descending
        request = self.factory.get(
            '/occurrences', {'ordering': '-start_time'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), TaskOccurrence.objects.count())
        self.assertEqual('06:00:00', response.data[0]['start_time'])
        self.assertEqual('01:00:00', response.data[-1]['start_time'])

        # test sorting by end_time descending
        request = self.factory.get(
            '/occurrences', {'ordering': '-end_time'})
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), TaskOccurrence.objects.count())
        self.assertEqual('16:00:00', response.data[0]['end_time'])
        self.assertEqual('11:00:00', response.data[-1]['end_time'])
