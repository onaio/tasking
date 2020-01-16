"""
Test for LocationType Serializers
"""
from tests.base import TestBase

from tasking.serializers import LocationTypeSerializer


class TestLocationTypeSerializer(TestBase):
    """
    Test the LocationType Serializer
    """

    def test_create_locationtype(self):
        """
        Test that the serializer can create LocationType objects
        """

        data = {
            'name': "Household",
        }

        serializer_instance = LocationTypeSerializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        locationtype = serializer_instance.save()

        self.assertDictContainsSubset(data, serializer_instance.data)
        self.assertEqual('Household', locationtype.name)

        expected_fields = [
            'id',
            'name',
        ]

        self.assertEqual(set(expected_fields),
                         set(list(serializer_instance.data.keys())))
