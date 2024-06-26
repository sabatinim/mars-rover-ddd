from typing import List, Dict

from app.ddd.command_dispatcher import InMemoryCommandDispatcher, InMemoryCommandDispatcherBuilder
from app.command_handler.commands import TurnRight, TurnLeft, Move, StartMarsRover, NotifyObstacle
from app.command_handler.move_command_handlers import MoveCommandHandler
from app.command_handler.notify_obstacle_command_handler import NotifyObstacleCommandHandler
from app.command_handler.start_mars_rover_command_handlers import StartMarsRoverCommandHandler
from app.command_handler.turn_left_command_handlers import TurnLeftCommandHandler
from app.command_handler.turn_right_command_handlers import TurnRightCommandHandler
from app.projection.mars_rover_path_projection import MarsRoverPathProjection
from app.projection.mars_rover_start_projection import MarsRoverStartProjection
from app.policy.policies import NotifyObstacleFoundPolicy
from app.domain.events import MarsRoverMoved, ObstacleFound, MarsRoverStarted
from app.infrastructure.mars_rover_repository import MarsRoverRepository


def create_command_dispatcher(repository: MarsRoverRepository,
                              path_projection_storage: List[Dict]) -> InMemoryCommandDispatcher:
    turn_right_command_handler = TurnRightCommandHandler(repo=repository)
    turn_left_command_handler = TurnLeftCommandHandler(repo=repository)
    move_command_handler = MoveCommandHandler(repo=repository)
    start_command_handler = StartMarsRoverCommandHandler(repo=repository)
    notify_obstacle_command_handler = NotifyObstacleCommandHandler()

    rover_path_projection = MarsRoverPathProjection(repo=repository, storage=path_projection_storage)
    rover_start_projection = MarsRoverStartProjection(repo=repository, storage=path_projection_storage)

    obstacle_found_policy = NotifyObstacleFoundPolicy()

    return (InMemoryCommandDispatcherBuilder()
            .with_command_handler(TurnRight, turn_right_command_handler)
            .with_command_handler(TurnLeft, turn_left_command_handler)
            .with_command_handler(Move, move_command_handler)
            .with_command_handler(StartMarsRover, start_command_handler)
            .with_command_handler(NotifyObstacle, notify_obstacle_command_handler)
            .with_projection(MarsRoverStarted, rover_start_projection)
            .with_projection(MarsRoverMoved, rover_path_projection)
            .with_policy(ObstacleFound, obstacle_found_policy)
            .build())
