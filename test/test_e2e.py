import unittest

from app.domain.mars_rover import MarsRover
from app.domain.mars_rover_id import MarsRoverId
from app.factory import create_mars_rover_executor, create_mars_rover_starter
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.service.mars_rover_executor import MarsRoverRunner
from app.service.mars_rover_starter import MarsRoverStarter


class TestE2E(unittest.TestCase):
    def test_execute_some_commands(self):
        repo = MarsRoverRepository()
        projections_storage = []

        starter: MarsRoverStarter = create_mars_rover_starter(repository=repo, storage=projections_storage)
        starter.start()

        id = next(iter(projections_storage)).get("id")

        executor: MarsRoverRunner = create_mars_rover_executor(repository=repo, storage=projections_storage)
        executor.run(id, "RMLMM")

        actual: MarsRover = repo.get_by_id(MarsRoverId(id))
        self.assertEqual("1:2:N", actual.coordinate())
        self.assertEqual("MOVING", actual.status.value)

        expected_path = ["0:0:N", "0:0:E", "1:0:E", "1:0:N", "1:1:N", "1:2:N"]
        actual_path = [p["actual_point"] for p in projections_storage]

        self.assertEqual(expected_path, actual_path)

    def test_hit_obstacle(self):
        repo = MarsRoverRepository()
        projections_storage = []

        starter: MarsRoverStarter = create_mars_rover_starter(repository=repo, storage=projections_storage)
        starter.start()

        id = next(iter(projections_storage)).get("id")

        executor: MarsRoverRunner = create_mars_rover_executor(repository=repo, storage=projections_storage)
        executor.run(id, "RMMLMMMMMM")

        actual: MarsRover = repo.get_by_id(MarsRoverId(id))
        self.assertEqual("O:2:1:N", actual.coordinate())
        self.assertEqual("TURNED_OFF", actual.status.value)

        expected_path = ["0:0:N", "0:0:E", "1:0:E", "2:0:E", "2:0:N", "2:1:N"]
        actual_path = [p["actual_point"] for p in projections_storage]

        self.assertEqual(expected_path, actual_path)
