import dataclasses

from app.ddd.basics import Event


@dataclasses.dataclass
class MarsRoverTurnedRight(Event):
    pass


@dataclasses.dataclass
class MarsRoverTurnedLeft(Event):
    pass


@dataclasses.dataclass
class MarsRoverMoved(Event):
    pass
