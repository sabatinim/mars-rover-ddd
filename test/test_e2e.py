import unittest

from app.domain.mars_rover import MarsRover, MarsRoverId
from app.factory import create_mars_rover, create_mars_rover_executor
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.service.mars_rover_executor import MarsRoverExecutor


class TestE2E(unittest.TestCase):
    def test_execute_some_commands(self):
        repo = MarsRoverRepository()
        path_storage = []
        mars_rover = create_mars_rover(rover_id=MarsRoverId("aaa"))
        repo.save(mars_rover)

        executor: MarsRoverExecutor = create_mars_rover_executor(repository=repo,
                                                                 storage=path_storage)

        executor.run("RMLMM")

        actual: MarsRover = repo.get_mars_rover()
        self.assertEqual(actual.coordinate(), "1:2:N")

        expected_path = [{'actual_point': '0:0:E', 'id': 'aaa'},
                         {'actual_point': '1:0:E', 'id': 'aaa'},
                         {'actual_point': '1:0:N', 'id': 'aaa'},
                         {'actual_point': '1:1:N', 'id': 'aaa'},
                         {'actual_point': '1:2:N', 'id': 'aaa'}]

        self.assertEqual(path_storage, expected_path)
