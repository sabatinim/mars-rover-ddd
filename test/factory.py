from app.domain.commands import Point, Direction
from app.domain.mars_rover import MarsRoverId, MarsRoverAgg


def create_mars_rover_agg(actual_point:Point = None):
    rover_id = MarsRoverId.new()
    if actual_point is None:
        actual_point = Point.create(0, 0, Direction.NORTH)
    grid = (4, 4)
    return MarsRoverAgg.create(rover_id, actual_point, grid)
