import dataclasses
from typing import Tuple

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
    coordinate: Tuple[int, int]

    @staticmethod
    def create(id: MarsRoverId, coordinate: Tuple[int, int]) -> 'ObstacleFound':
        return ObstacleFound(id=id, coordinate=coordinate)


@dataclasses.dataclass
class MarsRoverTurnedOff(Event):
    id: MarsRoverId

    @staticmethod
    def create(id: MarsRoverId) -> 'MarsRoverTurnedOff':
        return MarsRoverTurnedOff(id=id)


@dataclasses.dataclass
class ObstacleNotified(Event):
    pass
