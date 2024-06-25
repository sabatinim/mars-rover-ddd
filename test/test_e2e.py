import unittest

from app.domain.command_handlers import MarsRoverExecutor
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from test.factory import create_mars_rover_agg


class TestE2E(unittest.TestCase):
    def test_turn_right(self):
        repo = MarsRoverRepository()
        mars_rover = create_mars_rover_agg()
        repo.save(mars_rover)

        executor = MarsRoverExecutor(repo)

        executor.run("R")

        actual = repo.get_mars_rover()
        self.assertEqual(actual.coordinate(), "0:0:E")

    def test_turn_left(self):
        repo = MarsRoverRepository()
        mars_rover = create_mars_rover_agg()
        repo.save(mars_rover)

        executor = MarsRoverExecutor(repo)

        executor.run("L")

        actual = repo.get_mars_rover()
        self.assertEqual(actual.coordinate(), "0:0:W")

    def test_move(self):
        repo = MarsRoverRepository()
        mars_rover = create_mars_rover_agg()
        repo.save(mars_rover)

        executor = MarsRoverExecutor(repo)
        executor.run("MM")
        actual = repo.get_mars_rover()
        self.assertEqual(actual.coordinate(), "0:2:N")
