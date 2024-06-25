from app.domain.mars_rover import Point, Direction, MarsRover, MarsRoverId, World


def create_mars_rover(actual_point: Point = None,
                      direction: Direction = None,
                      world=None) -> MarsRover:
    rover_id = MarsRoverId.new()

    if actual_point is None:
        actual_point = Point.create(0, 0)

    if direction is None:
        direction = Direction.NORTH

    if world is None:
        world = World.create(dimension=(4, 4))

    return MarsRover.create(rover_id, actual_point, direction, world)
