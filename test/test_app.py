import enum
import unittest


class Point:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def to_string(self):
        return f"{self.x}:{self.y}:{self.direction.value}"


class TurnRight:
    @staticmethod
    def execute(previous_point: Point) -> Point:
        match previous_point.direction:
            case Direction.NORTH:
                return Point(previous_point.x, previous_point.y, Direction.EAST)


class TurnLeft:
    @staticmethod
    def execute(previous_point: Point) -> Point:
        match previous_point.direction:
            case Direction.NORTH:
                return Point(previous_point.x, previous_point.y, Direction.WEST)


class MarsRover:
    def __init__(self, initial_point):
        self.initial_point = initial_point

    def run(self, commands):
        for c in commands:
            match c:
                case "R":
                    self.initial_point = TurnRight.execute(self.initial_point)
                case "L":
                    self.initial_point = TurnLeft.execute(self.initial_point)
        return self.initial_point.to_string()


class Direction(enum.Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


class TestApp(unittest.TestCase):
    def test_turn_right(self):
        actual = MarsRover(initial_point=Point(0, 0, Direction.NORTH)).run("R")

        self.assertEqual(actual, "0:0:E")

    def test_turn_left(self):
        actual = MarsRover(initial_point=Point(0, 0, Direction.NORTH)).run("L")

        self.assertEqual(actual, "0:0:W")
