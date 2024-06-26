import dataclasses

from app.ddd.basics import Command
from app.domain.mars_rover.direction import Direction
from app.domain.mars_rover.mars_rover_id import MarsRoverId
from app.domain.mars_rover.point import Point
from app.domain.mars_rover.world import World


@dataclasses.dataclass
class StartMarsRover(Command):
    initial_point: Point
    initial_direction: Direction
    world: World



@dataclasses.dataclass
class TurnRight(Command):
    id: MarsRoverId


@dataclasses.dataclass
class TurnLeft(Command):
    id: MarsRoverId


@dataclasses.dataclass
class Move(Command):
    id: MarsRoverId


@dataclasses.dataclass
class NotifyObstacle(Command):
    message: str
