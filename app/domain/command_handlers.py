from functools import reduce

from app.domain.commands import TurnRight, TurnLeft, Move, Point


class MarsRover:
    def __init__(self, actual_point: Point, grid):
        self.actual_point = actual_point

        self.command_map = {"R": TurnRight(), "L": TurnLeft(), "M": Move(grid)}

    def run(self, commands):
        parsed_commands = [self.command_map[c] for c in commands]

        self.actual_point = reduce(lambda point, command: command.execute(point),
                                   parsed_commands,
                                   self.actual_point)

        return self.actual_point.to_string()
