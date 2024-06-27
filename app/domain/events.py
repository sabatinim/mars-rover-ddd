import dataclasses

from app.ddd.basics import Event
from app.domain.mars_rover_id import MarsRoverId


@dataclasses.dataclass
class MarsRoverStarted(Event):
    id: MarsRoverId

    @staticmethod
    def create(id: MarsRoverId) -> 'MarsRoverStarted':
        return MarsRoverStarted(id=id)


@dataclasses.dataclass
class MarsRoverMoved(Event):
    id: MarsRoverId

    @staticmethod
    def create(id: MarsRoverId) -> 'MarsRoverMoved':
        return MarsRoverMoved(id=id)


@dataclasses.dataclass
class ObstacleFound(Event):
    id: MarsRoverId

    @staticmethod
    def create(id: MarsRoverId) -> 'ObstacleFound':
        return ObstacleFound(id=id)


@dataclasses.dataclass
class MarsRoverTurnedOff(Event):
    id: MarsRoverId

    @staticmethod
    def create(id: MarsRoverId) -> 'MarsRoverTurnedOff':
        return MarsRoverTurnedOff(id=id)


@dataclasses.dataclass
class ObstacleNotified(Event):
    pass
