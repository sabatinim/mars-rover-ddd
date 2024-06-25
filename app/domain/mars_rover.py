import dataclasses
from typing import Tuple

from app.ddd.basics import AggregateId, Aggregate
from app.domain.commands import Point, Direction


class MarsRoverId(AggregateId):
    pass


@dataclasses.dataclass
class MarsRoverAgg(Aggregate):
    actual_point: Point
    grid: Tuple[int, int]

    def turn_right(self):
        match self.actual_point.direction:
            case Direction.NORTH:
                self.actual_point = Point(self.actual_point.x,
                                          self.actual_point.y,
                                          Direction.EAST)

    def turn_left(self):
        match self.actual_point.direction:
            case Direction.NORTH:
                self.actual_point = Point(self.actual_point.x,
                                          self.actual_point.y,
                                          Direction.WEST)

    def move(self):
        match self.actual_point.direction:
            case Direction.NORTH:
                self.actual_point = Point(self.actual_point.x, self.actual_point.y + 1, self.actual_point.direction)
            case Direction.EAST:
                self.actual_point = Point(self.actual_point.x + 1, self.actual_point.y, self.actual_point.direction)
            case Direction.WEST:
                x = self.grid[0] - abs(self.actual_point.x - 1)
                self.actual_point = Point(x, self.actual_point.y, self.actual_point.direction)

    def coordinate(self):
        return self.actual_point.to_string()

    @staticmethod
    def create(id: MarsRoverId, actual_point: Point, grid):
        return MarsRoverAgg(id=id,
                            version=0,
                            actual_point=actual_point,
                            grid=grid)
