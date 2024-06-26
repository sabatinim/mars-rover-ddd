import unittest

from app.command_handler.commands import TurnRight, TurnLeft, Move, StartMarsRover
from app.domain.events import MarsRoverMoved, MarsRoverStarted
from app.domain.direction import Direction
from app.domain.mars_rover import MarsRover
from app.domain.obstacles import Obstacles
from app.domain.point import Point
from app.domain.world import World
from app.command_handler.move_command_handlers import MoveCommandHandler
from app.command_handler.start_mars_rover_command_handlers import StartMarsRoverCommandHandler
from app.command_handler.turn_left_command_handlers import TurnLeftCommandHandler
from app.command_handler.turn_right_command_handlers import TurnRightCommandHandler
from app.factory import create_mars_rover
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class TestMarsCommandHandler(unittest.TestCase):
    def test_start_command_handler(self):
        repo = MarsRoverRepository()
        start_rover: StartMarsRover = _start_rover_command()

        event = StartMarsRoverCommandHandler(repo=repo).handle(command=start_rover)

        self.assertIsInstance(event, MarsRoverStarted)
        mars_rover: MarsRover = repo.get_by_id(event.id)
        self.assertEqual(1, mars_rover.version)
        self.assertEqual("STARTED", mars_rover.status.value)

    def test_turn_right_command_handler(self):
        repo, id = self._setup()

        event = TurnRightCommandHandler(repo=repo).handle(TurnRight(id=id))

        self.assertIsInstance(event, MarsRoverMoved)
        self._assert_aggregate(event, repo)

    def test_turn_left_command_handler(self):
        repo, id = self._setup()

        event = TurnLeftCommandHandler(repo=repo).handle(TurnLeft(id=id))

        self.assertIsInstance(event, MarsRoverMoved)
        self._assert_aggregate(event, repo)

    def test_move_command_handler(self):
        repo, id = self._setup()

        event = MoveCommandHandler(repo=repo).handle(Move(id=id))

        self.assertIsInstance(event, MarsRoverMoved)
        self._assert_aggregate(event, repo)

    def _setup(self):
        repo = MarsRoverRepository()
        mars_rover: MarsRover = create_mars_rover()
        repo.save(mars_rover)
        return repo, mars_rover.id

    def _assert_aggregate(self, event, repo):
        mars_rover: MarsRover = repo.get_by_id(event.id)
        self.assertEqual(2, mars_rover.version)
        self.assertEqual("MOVING", mars_rover.status.value)


def _start_rover_command():
    world = World.create(dimension=(4, 4),
                         obstacles=Obstacles.create(points=[]))
    start_rover = StartMarsRover(initial_point=Point.create(0, 0),
                                 initial_direction=Direction.NORTH,
                                 world=world)
    return start_rover
