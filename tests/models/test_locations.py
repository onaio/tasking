"""
Test for Location model
"""
from django.test import TestCase

from model_mommy import mommy


class TestLocations(TestCase):
    """
    Test class for Location models
    """

    def test_location_model_str(self):
        """
        Test the str method on Location model with Country Defined
        """
        nairobi = mommy.make("tasking.Location", name="Nairobi", country="KE")
        expected = "Kenya - Nairobi"
        self.assertEqual(expected, nairobi.__str__())

    def test_location_model_str_no_country(self):
        """
        Test the str method on Location model without Country Defined
        """
        nairobi = mommy.make("tasking.Location", name="Nairobi")
        expected = "Nairobi"
        self.assertEqual(expected, nairobi.__str__())

    def test_location_parent_link(self):
        """
        Test the parent link between Locations
        """
        nairobi = mommy.make("tasking.Location", name="Nairobi")
        hurlingham = mommy.make("tasking.Location", name="Hurlingham", parent=nairobi)
        self.assertEqual(nairobi, hurlingham.parent)
