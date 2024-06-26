from typing import List, Dict

from app.ddd.command_dispatcher import InMemoryCommandDispatcher
from app.domain.commands import StartMarsRover
from app.domain.mars_rover.direction import Direction
from app.domain.mars_rover.obstacles import Obstacles
from app.domain.mars_rover.point import Point
from app.domain.mars_rover.world import World
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.workflow_factory import create_command_dispatcher


class MarsRoverStarter:
    def __init__(self, repository: MarsRoverRepository, storage: List[Dict]):
        self.command_dispatcher: InMemoryCommandDispatcher = create_command_dispatcher(repository, storage)

    def start(self):
        initial_point = Point.create(0, 0)
        initial_direction = Direction.NORTH
        obstacles = Obstacles.create(points=[Point.create(2, 2)])
        world = World.create(dimension=(4, 4), obstacles=obstacles)

        start = StartMarsRover(initial_point=initial_point,
                               initial_direction=initial_direction,
                               world=world)
        self.command_dispatcher.submit([start])
        self.command_dispatcher.run()
