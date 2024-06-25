import dataclasses
import enum
from typing import Tuple

from app.ddd.basics import AggregateId, Aggregate


class Direction(enum.Enum):
    NORTH = "N"
    WEST = "W"
    EAST = "E"
    SOUTH = "S"


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
class World:
    dimension: Tuple[int, int]

    @staticmethod
    def create(dimension: Tuple[int, int]):
        return World(dimension=dimension)


@dataclasses.dataclass
class MarsRover(Aggregate):
    actual_point: Point
    direction: Direction
    world: World

    def turn_right(self):
        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.EAST
            case Direction.SOUTH:
                self.direction = Direction.WEST
            case Direction.WEST:
                self.direction = Direction.NORTH
            case Direction.EAST:
                self.direction = Direction.SOUTH

    def turn_left(self):
        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.WEST
            case Direction.SOUTH:
                self.direction = Direction.EAST
            case Direction.WEST:
                self.direction = Direction.SOUTH
            case Direction.EAST:
                self.direction = Direction.NORTH

    def move(self):
        match self.direction:
            case Direction.NORTH:
                self.actual_point.y = (self.actual_point.y + 1) % self.world.dimension[1]
            case Direction.SOUTH:
                self.actual_point.y = (self.actual_point.y - 1) % self.world.dimension[1]
            case Direction.WEST:
                self.actual_point.x = (self.actual_point.x - 1) % self.world.dimension[0]
            case Direction.EAST:
                self.actual_point.x = (self.actual_point.x + 1) % self.world.dimension[0]

    def coordinate(self):
        return f"{self.actual_point.x}:{self.actual_point.y}:{self.direction.value}"

    @staticmethod
    def create(id: MarsRoverId, actual_point: Point, direction: Direction, world: World):
        return MarsRover(id=id,
                         version=0,
                         actual_point=actual_point,
                         world=world,
                         direction=direction)
