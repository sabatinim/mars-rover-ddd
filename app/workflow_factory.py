from typing import List, Dict

from app.command_handler.commands import TurnRight, TurnLeft, Move, StartMarsRover, NotifyObstacle, TurnOff
from app.command_handler.move_command_handlers import MoveCommandHandler
from app.command_handler.notify_obstacle_command_handler import NotifyObstacleCommandHandler
from app.command_handler.start_mars_rover_command_handlers import StartMarsRoverCommandHandler
from app.command_handler.turn_left_command_handlers import TurnLeftCommandHandler
from app.command_handler.turn_off_command_handlers import TurnOffCommandHandler
from app.command_handler.turn_right_command_handlers import TurnRightCommandHandler
from app.ddd.command_dispatcher import InMemoryCommandDispatcher, InMemoryCommandDispatcherBuilder
from app.domain.events import MarsRoverMoved, ObstacleFound, MarsRoverStarted
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.policy.policies import NotifyObstacleFoundPolicy, TurnOffPolicy
from app.projection.mars_rover_ostacles_projection import MarsRoverObstaclesProjection
from app.projection.mars_rover_path_projection import MarsRoverPathProjection
from app.projection.mars_rover_start_projection import MarsRoverStartProjection


def create_command_dispatcher(mars_rover_repo: MarsRoverRepository,
                              mars_rover_start_view: List[MarsRoverId],
                              mars_rover_path_view: List[Dict],
                              obstacle_view: List[Dict]) -> InMemoryCommandDispatcher:
    turn_right_command_handler = TurnRightCommandHandler(repo=mars_rover_repo)
    turn_left_command_handler = TurnLeftCommandHandler(repo=mars_rover_repo)
    move_command_handler = MoveCommandHandler(repo=mars_rover_repo)
    start_command_handler = StartMarsRoverCommandHandler(repo=mars_rover_repo)
    turn_off_command_handler = TurnOffCommandHandler(repo=mars_rover_repo)
    notify_obstacle_command_handler = NotifyObstacleCommandHandler()

    rover_start_projection = MarsRoverStartProjection(repo=mars_rover_repo,
                                                      paths_storage=mars_rover_path_view,
                                                      mars_rover_storage=mars_rover_start_view)
    rover_path_projection = MarsRoverPathProjection(repo=mars_rover_repo, storage=mars_rover_path_view)
    rover_obstacles_projection = MarsRoverObstaclesProjection(storage=obstacle_view)

    obstacle_found_policy = NotifyObstacleFoundPolicy()
    turn_off_policy = TurnOffPolicy()

    return (InMemoryCommandDispatcherBuilder()
            .with_command_handler(TurnRight, turn_right_command_handler)
            .with_command_handler(TurnLeft, turn_left_command_handler)
            .with_command_handler(Move, move_command_handler)
            .with_command_handler(StartMarsRover, start_command_handler)
            .with_command_handler(TurnOff, turn_off_command_handler)
            .with_command_handler(NotifyObstacle, notify_obstacle_command_handler)
            .with_projection(MarsRoverStarted, rover_start_projection)
            .with_projection(MarsRoverMoved, rover_path_projection)
            .with_projection(ObstacleFound, rover_obstacles_projection)
            .with_policy(ObstacleFound, obstacle_found_policy)
            .with_policy(ObstacleFound, turn_off_policy)
            .build())
