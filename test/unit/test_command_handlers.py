import unittest

from app.domain.commands import TurnRight, TurnLeft, Move
from app.domain.events import MarsRoverMoved
from app.domain.mars_rover.mars_rover import MarsRover
from app.domain.mars_rover.mars_rover_id import MarsRoverId
from app.domain.move_command_handlers import MoveCommandHandler
from app.domain.turn_left_command_handlers import TurnLeftCommandHandler
from app.domain.turn_right_command_handlers import TurnRightCommandHandler
from app.factory import create_mars_rover
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class TestMarsCommandHandler(unittest.TestCase):
    def test_turn_right_command_handler(self):
        repo = self._setup()

        event = TurnRightCommandHandler(repo=repo).handle(TurnRight(MarsRoverId(value='aaa')))

        self._assert_event(event)
        self._assert_version(repo)

    def test_turn_left_command_handler(self):
        repo = self._setup()

        event = TurnLeftCommandHandler(repo=repo).handle(TurnLeft(MarsRoverId(value='aaa')))

        self._assert_event(event)
        self._assert_version(repo)

    def test_move_command_handler(self):
        repo = self._setup()

        event = MoveCommandHandler(repo=repo).handle(Move(MarsRoverId(value='aaa')))

        self._assert_event(event)
        self._assert_version(repo)

    def _setup(self):
        repo = MarsRoverRepository()
        mars_rover: MarsRover = create_mars_rover(rover_id=MarsRoverId("aaa"))
        repo.save(mars_rover)
        return repo

    def _assert_version(self, repo):
        mars_rover: MarsRover = repo.get_mars_rover()
        self.assertEqual(2, mars_rover.version)

    def _assert_event(self, event):
        expected = MarsRoverMoved(id=MarsRoverId(value='aaa'))
        self.assertEqual(expected, event)
