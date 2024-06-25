import dataclasses
import enum
from typing import Tuple

from app.ddd.basics import AggregateId, Aggregate


class Direction(enum.Enum):
    NORTH = "N"
    WEST = "W"
    EAST = "E"


@dataclasses.dataclass
class Point:
    x: int
    y: int

    @staticmethod
    def create(x, y):
        return Point(x=x, y=y)


class MarsRoverId(AggregateId):
    pass


@dataclasses.dataclass
class MarsRover(Aggregate):
    actual_point: Point
    direction: Direction
    grid: Tuple[int, int]

    def turn_right(self):
        match self.direction:
            case Direction.NORTH:
                self.actual_point = Point(self.actual_point.x, self.actual_point.y)
                self.direction = Direction.EAST

    def turn_left(self):
        match self.direction:
            case Direction.NORTH:
                self.actual_point = Point(self.actual_point.x, self.actual_point.y)
                self.direction = Direction.WEST

    def move(self):
        match self.direction:
            case Direction.NORTH:
                self.actual_point = Point(self.actual_point.x, self.actual_point.y + 1)
            case Direction.EAST:
                self.actual_point = Point(self.actual_point.x + 1, self.actual_point.y)
            case Direction.WEST:
                x = self.grid[0] - abs(self.actual_point.x - 1)
                self.actual_point = Point(x, self.actual_point.y)

    def coordinate(self):
        return f"{self.actual_point.x}:{self.actual_point.y}:{self.direction.value}"

    @staticmethod
    def create(id: MarsRoverId, actual_point: Point, direction: Direction, grid):
        return MarsRover(id=id,
                         version=0,
                         actual_point=actual_point,
                         grid=grid,
                         direction=direction)
