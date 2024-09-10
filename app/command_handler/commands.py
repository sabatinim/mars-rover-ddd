import dataclasses

from app.ddd.basics import Command
from app.domain.direction import Direction
from app.domain.mars_rover_id import MarsRoverId
from app.domain.point import Point
from app.domain.world import World


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
class TurnOff(Command):
    id: MarsRoverId


@dataclasses.dataclass
class NotifyObstacleHit(Command):
    message: str
