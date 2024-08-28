from typing import List, Dict, Tuple, Set

from app.command_handler.commands import TurnRight, TurnLeft, Move, StartMarsRover, NotifyObstacleHit
from app.command_handler.move_command_handlers import MoveCommandHandler
from app.command_handler.notify_obstacle_command_handler import NotifyObstacleCommandHandler
from app.command_handler.start_mars_rover_command_handlers import StartMarsRoverCommandHandler
from app.command_handler.turn_left_command_handlers import TurnLeftCommandHandler
from app.command_handler.turn_right_command_handlers import TurnRightCommandHandler
from app.ddd.command_dispatcher import InMemoryCommandDispatcher
from app.ddd.command_dispatcher_builder import InMemoryCommandDispatcherBuilder
from app.domain.events import MarsRoverMoved, ObstacleHit, MarsRoverStarted
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository
from app.policy.policies import NotifyObstacleHitPolicy
from app.projection.mars_rover_ostacles_projection import MarsRoverObstaclesProjection
from app.projection.mars_rover_path_projection import MarsRoverPathProjection
from app.projection.mars_rover_start_projection import MarsRoverStartProjection


def create_command_dispatcher(mars_rover_repo: InMemoryMarsRoverRepository,
                              mars_rover_start_view: List[MarsRoverId],
                              mars_rover_path_view: List[Dict],
                              obstacle_view: Set[Tuple[int, int]]) -> InMemoryCommandDispatcher:
    start = StartMarsRoverCommandHandler(repo=mars_rover_repo)
    turn_right = TurnRightCommandHandler(repo=mars_rover_repo)
    turn_left = TurnLeftCommandHandler(repo=mars_rover_repo)
    move = MoveCommandHandler(repo=mars_rover_repo)
    notify_obstacle = NotifyObstacleCommandHandler()

    notify_obstacle_policy = NotifyObstacleHitPolicy()

    start_projection = MarsRoverStartProjection(repo=mars_rover_repo,
                                                mars_rover_path_view=mars_rover_path_view,
                                                mars_rover_start_view=mars_rover_start_view)
    path_projection = MarsRoverPathProjection(repo=mars_rover_repo,
                                              mars_rover_path_view=mars_rover_path_view)
    obstacles_projection = MarsRoverObstaclesProjection(obstacle_view=obstacle_view)

    return (InMemoryCommandDispatcherBuilder()
            .with_command_handler(StartMarsRover, start)
            .with_command_handler(TurnRight, turn_right)
            .with_command_handler(TurnLeft, turn_left)
            .with_command_handler(Move, move)
            .with_command_handler(NotifyObstacleHit, notify_obstacle)
            .with_policy(ObstacleHit, notify_obstacle_policy)
            .with_projection(MarsRoverStarted, start_projection)
            .with_projection(MarsRoverMoved, path_projection)
            .with_projection(ObstacleHit, obstacles_projection)
            .build())
