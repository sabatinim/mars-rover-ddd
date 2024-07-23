import unittest

from _pytest.outcomes import fail

from app.ddd.generic_aggregate_repository import ConcurrencyException
from app.factory import create_mars_rover
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository


class TestMarsRoverRepository(unittest.TestCase):
    def test_save_mars_rover_aggregate(self):
        mars_rover = create_mars_rover()
        repository = InMemoryMarsRoverRepository()
        repository.save(mars_rover)

        actual = repository.get_by_id(mars_rover.id)

        self.assertIsNotNone(actual)

    def test_save_same_version(self):
        repository = InMemoryMarsRoverRepository()

        mars_rover = create_mars_rover()
        repository.save(mars_rover)
        try:
            repository.save(mars_rover)
            fail("Should catch exception!")
            fail("Should catch exception!")
        except ConcurrencyException as e:
            self.assertEqual(str(e), "Optimistic concurrency control check failed")
