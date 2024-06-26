import unittest

from app.domain.mars_rover.mars_rover import MarsRover
from app.domain.mars_rover.mars_rover_id import MarsRoverId
from app.domain.mars_rover.obstacles import Obstacles
from app.domain.mars_rover.point import Point
from app.factory import create_mars_rover, create_mars_rover_executor
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.service.mars_rover_executor import MarsRoverExecutor


class TestE2E(unittest.TestCase):
    def test_execute_some_commands(self):
        repo = MarsRoverRepository()
        path_storage = []

        mars_rover: MarsRover = create_mars_rover(rover_id=MarsRoverId("aaa"))
        repo.save(mars_rover)

        executor: MarsRoverExecutor = create_mars_rover_executor(repository=repo,
                                                                 storage=path_storage)

        executor.run("aaa", "RMLMM")

        actual: MarsRover = repo.get_mars_rover()
        self.assertEqual("1:2:N", actual.coordinate())

        expected_path = [{'actual_point': '0:0:E', 'id': 'aaa'},
                         {'actual_point': '1:0:E', 'id': 'aaa'},
                         {'actual_point': '1:0:N', 'id': 'aaa'},
                         {'actual_point': '1:1:N', 'id': 'aaa'},
                         {'actual_point': '1:2:N', 'id': 'aaa'}]

        self.assertEqual(expected_path, path_storage)

    def test_hit_obstacle(self):
        repo = MarsRoverRepository()
        path_storage = []

        mars_rover: MarsRover = create_mars_rover(rover_id=MarsRoverId("aaa"),
                                                  obstacles=Obstacles.create(points=[Point.create(1, 1)]))
        repo.save(mars_rover)

        executor: MarsRoverExecutor = create_mars_rover_executor(repository=repo,
                                                                 storage=path_storage)

        executor.run("aaa", "RMLMMMMMM")

        actual: MarsRover = repo.get_mars_rover()
        self.assertEqual("O:1:0:N", actual.coordinate())

        expected_path = [{'actual_point': '0:0:E', 'id': 'aaa'},
                         {'actual_point': '1:0:E', 'id': 'aaa'},
                         {'actual_point': '1:0:N', 'id': 'aaa'}]

        self.assertEqual(expected_path, path_storage)
