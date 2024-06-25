import dataclasses
import enum


class Direction(enum.Enum):
    NORTH = "N"
    WEST = "W"
    EAST = "E"


@dataclasses.dataclass
class Point:
    x: int
    y: int
    direction: Direction

    @staticmethod
    def create(x, y, direction: Direction):
        return Point(x=x, y=y, direction=direction)

    def to_string(self):
        return f"{self.x}:{self.y}:{self.direction.value}"


class TurnRight:
    def execute(self, previous_point: Point) -> Point:
        match previous_point.direction:
            case Direction.NORTH:
                return Point(previous_point.x, previous_point.y, Direction.EAST)


class TurnLeft:
    def execute(self, previous_point: Point) -> Point:
        match previous_point.direction:
            case Direction.NORTH:
                return Point(previous_point.x, previous_point.y, Direction.WEST)


class Move:
    def __init__(self, grid):
        self.grid = grid

    def execute(self, previous_point: Point) -> Point:
        match previous_point.direction:
            case Direction.NORTH:
                return Point(previous_point.x, previous_point.y + 1, previous_point.direction)
            case Direction.EAST:
                return Point(previous_point.x + 1, previous_point.y, previous_point.direction)
            case Direction.WEST:
                x = self.grid[0] - abs(previous_point.x - 1)
                return Point(x, previous_point.y, previous_point.direction)
