import unittest

from app.domain.command_handlers import MarsRoverExecutor
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.factory import create_mars_rover


class TestE2E(unittest.TestCase):
    def test_execute_some_commands(self):
        repo = MarsRoverRepository()
        mars_rover = create_mars_rover()
        repo.save(mars_rover)

        executor = MarsRoverExecutor(repo)

        executor.run("RMLMM")

        actual = repo.get_mars_rover()
        self.assertEqual(actual.coordinate(), "1:2:N")
