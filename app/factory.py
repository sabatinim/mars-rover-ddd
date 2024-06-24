from app.domain.command_handlers import MarsRover
from app.domain.commands import Direction, Point


def create_mars_rover(actual_point=Point(0, 0, Direction.NORTH), grid=(4, 4)):
    return MarsRover(actual_point=actual_point, grid=grid)