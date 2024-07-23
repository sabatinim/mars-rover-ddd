import unittest

from app.domain.direction import Direction
from app.domain.mars_rover import MarsRover
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository
from app.service.mars_rover_runner import MarsRoverRunner


class TestE2E(unittest.TestCase):
    # x x x x
    # x x x x
    # x x x x
    # x x x x
    #
    def test_execute_some_commands(self):
        repo = InMemoryMarsRoverRepository()
        mars_rover_start_view = []
        mars_rover_path_view = []
        obstacle_view = []

        runner = (
            MarsRoverRunner(repository=repo,
                            mars_rover_start_view=mars_rover_start_view,
                            mars_rover_path_view=mars_rover_path_view,
                            obstacle_view=obstacle_view)
            .with_initial_point(x=0, y=0)
            .with_initial_direction(direction=Direction.NORTH)
            .with_world(world_dimension=(4, 4),
                        obstacles=[])
        )
        runner.start_rover()

        id = mars_rover_start_view[0]

        runner.execute(rover_id=id, commands="RMLMM")

        actual: MarsRover = repo.get_by_id(MarsRoverId(id))
        self.assertEqual("1:2:N", actual.coordinate())
        self.assertEqual("MOVING", actual.status.value)

        expected_path = ["0:0:N", "0:0:E", "1:0:E", "1:0:N", "1:1:N", "1:2:N"]
        self._assert_paths(expected=expected_path, actual=mars_rover_path_view)

        self.assertListEqual([], obstacle_view)

    # x x x x
    # x x o x
    # x x x x
    # x x x x
    #
    def test_hit_obstacle(self):
        repo = InMemoryMarsRoverRepository()
        mars_rover_start_view = []
        mars_rover_path_view = []
        obstacle_view = []

        runner = (
            MarsRoverRunner(repository=repo,
                            mars_rover_start_view=mars_rover_start_view,
                            mars_rover_path_view=mars_rover_path_view,
                            obstacle_view=obstacle_view)
            .with_initial_point(x=0, y=0)
            .with_initial_direction(direction=Direction.NORTH)
            .with_world(world_dimension=(4, 4),
                        obstacles=[(2, 2)])
        )

        runner.start_rover()

        id = mars_rover_start_view[0]

        runner.execute(rover_id=id, commands="RMMLMMMMMM")

        actual: MarsRover = repo.get_by_id(MarsRoverId(id))
        self.assertEqual("O:2:1:N", actual.coordinate())
        self.assertEqual("TURNED_OFF", actual.status.value)

        expected_path = ["0:0:N", "0:0:E", "1:0:E", "2:0:E", "2:0:N", "2:1:N"]
        self._assert_paths(expected=expected_path, actual=mars_rover_path_view)

        expected_obstacles = [(2, 2)]
        self._assert_obstacles(expected=expected_obstacles, actual=obstacle_view)

    def _assert_obstacles(self, expected, actual):
        obstacles_found = [o["obstacle"] for o in actual]
        self.assertEqual(expected, obstacles_found)

    def _assert_paths(self, expected, actual):
        actual_path = [p["actual_point"] for p in actual]
        self.assertEqual(expected, actual_path)
