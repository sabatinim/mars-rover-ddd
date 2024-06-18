import enum
import unittest
from functools import reduce


class Point:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

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


class MarsRover:
    def __init__(self, actual_point: Point, grid):
        self.actual_point = actual_point

        self.command_map = {"R": TurnRight(),
                            "L": TurnLeft(),
                            "M": Move(grid)}

    def run(self, commands):
        parsed_commands = [self.command_map[c] for c in commands]

        self.actual_point = reduce(lambda point, command: command.execute(point),
                                   parsed_commands,
                                   self.actual_point)

        return self.actual_point.to_string()


class Direction(enum.Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


class TestApp(unittest.TestCase):
    def test_turn_right(self):
        actual = create_mars_rover().run("R")

        self.assertEqual(actual, "0:0:E")

    def test_turn_left(self):
        actual = create_mars_rover().run("L")

        self.assertEqual(actual, "0:0:W")

    def test_move(self):
        actual = create_mars_rover().run("M")

        self.assertEqual(actual, "0:1:N")

    def test_move_double(self):
        actual = create_mars_rover().run("MM")

        self.assertEqual(actual, "0:2:N")

    def test_move_on_x(self):
        actual = create_mars_rover(actual_point=Point(0, 0, Direction.EAST)).run("MM")

        self.assertEqual(actual, "2:0:E")

    def test_move_on_y(self):
        actual = create_mars_rover(actual_point=Point(0, 0, Direction.WEST)).run("MM")

        self.assertEqual(actual, "2:0:W")


def create_mars_rover(actual_point=Point(0, 0, Direction.NORTH), grid=(4, 4)):
    return MarsRover(actual_point=actual_point, grid=grid)
