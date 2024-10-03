from typing import List, Dict, Tuple, Set

from app.command_handler.commands import TurnRight, TurnLeft, Move, StartMarsRover
from app.ddd.basics import Command
from app.ddd.command_dispatcher import InMemoryCommandDispatcher
from app.domain.direction import Direction
from app.domain.mars_rover_id import MarsRoverId
from app.domain.obstacles import Obstacles
from app.domain.point import Point
from app.domain.world import World
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository
from app.workflow_factory import create_command_dispatcher


class MarsRoverRunner:
    def __init__(self,
                 repository: InMemoryMarsRoverRepository,
                 mars_rover_path_view: List[Dict],
                 obstacle_view: Set[Tuple[int, int]],
                 mars_rover_start_view: List[MarsRoverId]):
        self.command_dispatcher: InMemoryCommandDispatcher = (
            create_command_dispatcher(mars_rover_repo=repository,
                                      mars_rover_path_view=mars_rover_path_view,
                                      obstacle_view=obstacle_view,
                                      mars_rover_start_view=mars_rover_start_view)
        )
        self.command_map = {"R": TurnRight, "L": TurnLeft, "M": Move}

    def with_initial_point(self, x: int, y: int):
        self.initial_point = Point.create(x, y)
        return self

    def with_initial_direction(self, direction: Direction):
        self.initial_direction = direction
        return self

    def with_world(self, obstacles: List[Tuple[int, int]], world_dimension: Tuple[int, int]):
        world_obstacles = Obstacles.create(points=[Point.create(o[0], o[1]) for o in obstacles])
        self.world = World.create(dimension=world_dimension, obstacles=world_obstacles)
        return self

    def start_rover(self):
        command = StartMarsRover(initial_point=self.initial_point,
                                 initial_direction=self.initial_direction,
                                 world=self.world)

        (self.command_dispatcher
         .submit(command)
         .run())

    def execute(self, rover_id: str, commands: str):
        commands: List[Command] = [self.command_map[c](MarsRoverId(rover_id)) for c in commands]
        for c in commands:
            (self.command_dispatcher
             .submit(command=c)
             .run())
