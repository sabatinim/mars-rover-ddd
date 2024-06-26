import dataclasses

from app.ddd.basics import Command
from app.domain.mars_rover.mars_rover_id import MarsRoverId


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
