import dataclasses

from app.ddd.basics import Event
from app.domain.mars_rover.mars_rover_id import MarsRoverId


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
class ObstacleNotified(Event):
    pass
