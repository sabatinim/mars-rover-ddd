import dataclasses
from typing import Tuple

from app.ddd.basics import AggregateId, Aggregate
from app.domain.commands import Point


class MarsRoverId(AggregateId):
    pass


@dataclasses.dataclass
class MarsRoverAgg(Aggregate):
    actual_point: Point
    grid: Tuple[int, int]

    @staticmethod
    def create(id: MarsRoverId, actual_point: Point, grid):
        return MarsRoverAgg(id=id,
                            version=0,
                            actual_point=actual_point,
                            grid=grid)
