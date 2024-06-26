from typing import List, Dict

from app.ddd.command_dispatcher import InMemoryCommandDispatcherBuilder, InMemoryCommandDispatcher
from app.domain.commands import TurnRight, TurnLeft, Move, NotifyObstacle
from app.domain.events import MarsRoverMoved, ObstacleFound
from app.domain.mars_rover.mars_rover_id import MarsRoverId
from app.domain.move_command_handlers import MoveCommandHandler
from app.domain.notify_obstacle_command_handler import NotifyObstacleCommandHandler
from app.domain.policies import NotifyObstacleFoundPolicy
from app.domain.turn_left_command_handlers import TurnLeftCommandHandler
from app.domain.turn_right_command_handlers import TurnRightCommandHandler
from app.infrastructure.mars_rover_path_projection import MarsRoverPathProjection
from app.infrastructure.mars_rover_repository import MarsRoverRepository


def create_command_dispatcher(repository: MarsRoverRepository,
                              path_projection_storage: List[Dict]) -> InMemoryCommandDispatcher:
    turn_right_command_handler = TurnRightCommandHandler(repo=repository)
    turn_left_command_handler = TurnLeftCommandHandler(repo=repository)
    move_command_handler = MoveCommandHandler(repo=repository)
    notify_obstacle_command_handler = NotifyObstacleCommandHandler()

    rover_path_projection = MarsRoverPathProjection(repo=repository, storage=path_projection_storage)

    obstacle_found_policy = NotifyObstacleFoundPolicy()

    return (InMemoryCommandDispatcherBuilder()
            .with_command_handler(TurnRight, turn_right_command_handler)
            .with_command_handler(TurnLeft, turn_left_command_handler)
            .with_command_handler(Move, move_command_handler)
            .with_command_handler(NotifyObstacle, notify_obstacle_command_handler)
            .with_projection(MarsRoverMoved, rover_path_projection)
            .with_policy(ObstacleFound, obstacle_found_policy)
            .build())


class MarsRoverExecutor:
    def __init__(self, repository: MarsRoverRepository, storage: List[Dict]):
        self.command_dispatcher: InMemoryCommandDispatcher = create_command_dispatcher(repository, storage)
        self.command_map = {"R": TurnRight, "L": TurnLeft, "M": Move}

    def run(self, rover_id: str, commands: str):
        parsed_commands = [self.command_map[c](MarsRoverId(rover_id)) for c in commands]

        self.command_dispatcher.submit(commands=parsed_commands)

        self.command_dispatcher.run()
