from app.domain.mars_rover import MarsRoverId, MarsRover, Direction, Point


def create_mars_rover_agg(actual_point: Point = None, direction: Direction = None):
    rover_id = MarsRoverId.new()
    if actual_point is None:
        actual_point = Point.create(0, 0)

    if direction is None:
        direction = Direction.NORTH

    grid = (4, 4)
    return MarsRover.create(rover_id, actual_point, direction, grid)
