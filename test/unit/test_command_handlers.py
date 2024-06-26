import unittest

from app.domain.commands import TurnRight, TurnLeft, Move, StartMarsRover
from app.domain.events import MarsRoverMoved, MarsRoverStarted
from app.domain.mars_rover.direction import Direction
from app.domain.mars_rover.mars_rover import MarsRover
from app.domain.mars_rover.mars_rover_id import MarsRoverId
from app.domain.mars_rover.obstacles import Obstacles
from app.domain.mars_rover.point import Point
from app.domain.mars_rover.world import World
from app.domain.move_command_handlers import MoveCommandHandler
from app.domain.start_mars_rover_command_handlers import StartMarsRoverCommandHandler
from app.domain.turn_left_command_handlers import TurnLeftCommandHandler
from app.domain.turn_right_command_handlers import TurnRightCommandHandler
from app.factory import create_mars_rover
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class TestMarsCommandHandler(unittest.TestCase):
    def test_start_command_handler(self):
        repo = MarsRoverRepository()

        world = World.create(dimension=(4, 4),
                             obstacles=Obstacles.create(points=[]))

        start_rover = StartMarsRover(initial_point=Point.create(0, 0),
                               initial_direction=Direction.NORTH,
                               world=world)

        event = StartMarsRoverCommandHandler(repo=repo).handle(command=start_rover)

        self.assertIsInstance(event, MarsRoverStarted)
        self.assertIsNotNone(event.id)
        self._assert_version(repo, exp=1)

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

    def _assert_version(self, repo, exp=2):
        mars_rover: MarsRover = repo.get_mars_rover()
        self.assertEqual(exp, mars_rover.version)

    def _assert_event(self, event):
        expected = MarsRoverMoved(id=MarsRoverId(value='aaa'))
        self.assertEqual(expected, event)
