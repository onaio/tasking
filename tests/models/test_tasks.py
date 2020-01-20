"""
Test for Task model
"""
from django.test import TestCase

from model_mommy import mommy


class TestTasks(TestCase):
    """
    Test class for task models
    """

    def test_task_model_str(self):
        """
        Test the str method on Task model
        """
        cow_price = mommy.make("tasking.Task", name="Cow prices")
        expected = f"Cow prices - {cow_price.pk}"
        self.assertEqual(expected, str(cow_price))

    def test_tasklocation_model_str(self):
        """
        Test __str__ on TaskLocation
        """
        self.assertEqual(
            "oGame at home",
            mommy.make(
                "tasking.TaskLocation",
                task=mommy.make("tasking.Task", name="oGame"),
                location=mommy.make("tasking.Location", name="home"),
                start="08:00:00",
                end="19:00:00",
            ).__str__(),
        )
