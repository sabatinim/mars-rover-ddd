from typing import List, Dict

from app.domain.direction import Direction
from app.domain.mars_rover import MarsRover
from app.domain.mars_rover_id import MarsRoverId
from app.domain.obstacles import Obstacles
from app.domain.point import Point
from app.domain.world import World
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.service.mars_rover_runner import MarsRoverRunner
from app.service.mars_rover_starter import MarsRoverStarter


def create_mars_rover(actual_point: Point = None,
                      direction: Direction = None,
                      world=None,
                      rover_id: MarsRoverId = None,
                      obstacles: Obstacles = None) -> MarsRover:
    if rover_id is None:
        rover_id = MarsRoverId.new()

    if actual_point is None:
        actual_point = Point.create(0, 0)

    if direction is None:
        direction = Direction.NORTH

    if obstacles is None:
        obstacles = Obstacles.create(points=[Point.create(2, 2)])

    if world is None:
        world = World.create(dimension=(4, 4), obstacles=obstacles)

    return MarsRover.create(rover_id, actual_point, direction, world)


def create_mars_rover_executor(repository: MarsRoverRepository, storage: List[Dict]) -> MarsRoverRunner:
    return MarsRoverRunner(repository=repository, storage=storage)


def create_mars_rover_starter(repository, storage) -> MarsRoverStarter:
    return MarsRoverStarter(repository=repository, storage=storage)
