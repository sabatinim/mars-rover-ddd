import unittest

from _pytest.outcomes import fail

from app.ddd.generic_aggregate_repository import ConcurrencyException
from app.domain.mars_rover import MarsRoverId, MarsRoverAgg, Direction, Point
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class TestMarsRoverRepository(unittest.TestCase):
    def test_save_mars_rover_aggregate(self):
        rover_id = MarsRoverId.new()
        actual_point = Point.create(0, 0, Direction.NORTH)
        grid = (4, 4)
        agg = MarsRoverAgg.create(rover_id, actual_point, grid)
        repository = MarsRoverRepository()
        repository.save(agg)

        actual = repository.get_by_id(rover_id)

        self.assertEqual(actual.id, rover_id)
        self.assertEqual(actual.version, 1)
        self.assertEqual(actual.actual_point, actual_point)
        self.assertEqual(actual.grid, grid)

    def test_save_same_version(self):
        rover_id = MarsRoverId.new()
        agg = MarsRoverAgg.create(rover_id, Point.create(0, 0, Direction.NORTH), (4, 4))
        repository = MarsRoverRepository()
        repository.save(agg)

        try:
            repository.save(agg)
            fail("Should catch exception!")
        except ConcurrencyException as e:
            self.assertEqual(str(e), "Optimistic concurrency control check failed")
