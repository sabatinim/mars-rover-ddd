import unittest

from app.factory import create_mars_rover, create_mars_rover_executor
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.service.mars_rover_executor import MarsRoverExecutor


class TestE2E(unittest.TestCase):
    def test_execute_some_commands(self):
        repo = MarsRoverRepository()
        mars_rover = create_mars_rover()
        repo.save(mars_rover)

        executor: MarsRoverExecutor = create_mars_rover_executor(repository=repo)

        executor.run("RMLMM")

        actual = repo.get_mars_rover()
        self.assertEqual(actual.coordinate(), "1:2:N")
