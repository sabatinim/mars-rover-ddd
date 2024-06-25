import dataclasses

from app.ddd.basics import Command


@dataclasses.dataclass
class TurnRight(Command):
    pass


@dataclasses.dataclass
class TurnLeft(Command):
    pass


@dataclasses.dataclass
class Move(Command):
    pass
