import unittest

from app.domain.direction import Direction
from app.domain.mars_rover import MarsRover
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.service.mars_rover_runner import MarsRoverRunner


class TestE2E(unittest.TestCase):
    def test_execute_some_commands(self):
        repo = MarsRoverRepository()
        paths = []
        obstacles = []
        mars_rover_ids = []

        runner = (
            MarsRoverRunner(repository=repo,
                            path_projection_storage=paths,
                            obstacles_projection_storage=obstacles,
                            mars_rover_projection_storage=mars_rover_ids)
            .with_initial_point(x=0, y=0)
            .with_initial_direction(direction=Direction.NORTH)
            .with_world(world_dimension=(4, 4),
                        obstacles=[])
        )
        runner.start()

        id = next(iter(paths)).get("id")

        runner.run(id, "RMLMM")

        actual: MarsRover = repo.get_by_id(MarsRoverId(id))
        self.assertEqual("1:2:N", actual.coordinate())
        self.assertEqual("MOVING", actual.status.value)

        expected_path = ["0:0:N", "0:0:E", "1:0:E", "1:0:N", "1:1:N", "1:2:N"]
        actual_path = [p["actual_point"] for p in paths]

        self.assertEqual(expected_path, actual_path)
        self.assertListEqual([], obstacles)

    def test_hit_obstacle(self):
        repo = MarsRoverRepository()
        paths = []
        obstacles = []
        mars_rover_ids = []

        runner = (
            MarsRoverRunner(repository=repo,
                            path_projection_storage=paths,
                            obstacles_projection_storage=obstacles,
                            mars_rover_projection_storage=mars_rover_ids)
            .with_initial_point(x=0, y=0)
            .with_initial_direction(direction=Direction.NORTH)
            .with_world(world_dimension=(4, 4),
                        obstacles=[(2, 2)])
        )

        runner.start()

        id = next(iter(paths)).get("id")

        runner.run(id, "RMMLMMMMMM")

        actual: MarsRover = repo.get_by_id(MarsRoverId(id))
        self.assertEqual("O:2:1:N", actual.coordinate())
        self.assertEqual("TURNED_OFF", actual.status.value)

        expected_path = ["0:0:N", "0:0:E", "1:0:E", "2:0:E", "2:0:N", "2:1:N"]
        actual_path = [p["actual_point"] for p in paths]

        self.assertEqual(expected_path, actual_path)

        obstacles_found = [o["obstacle"] for o in obstacles]
        self.assertEqual([(2, 2)], obstacles_found)
