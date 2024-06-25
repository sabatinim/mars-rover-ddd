import dataclasses

from app.ddd.basics import Event
from app.domain.mars_rover import MarsRoverId


@dataclasses.dataclass
class MarsRoverMoved(Event):
    id: MarsRoverId

    @staticmethod
    def create(id: MarsRoverId) -> 'MarsRoverMoved':
        return MarsRoverMoved(id=id)
