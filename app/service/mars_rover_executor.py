from typing import List, Dict

from app.ddd.command_dispatcher import InMemoryCommandDispatcherBuilder, InMemoryCommandDispatcher
from app.domain.command_handlers import TurnRightCommandHandler, TurnLeftCommandHandler, MoveCommandHandler
from app.domain.commands import TurnRight, TurnLeft, Move
from app.domain.events import MarsRoverMoved
from app.infrastructure.mars_rover_path_projection import MarsRoverPathProjection
from app.infrastructure.mars_rover_repository import MarsRoverRepository


def create_command_dispatcher(repository: MarsRoverRepository, storage: List[Dict]) -> InMemoryCommandDispatcher:
    turn_right_command_handler = TurnRightCommandHandler(repo=repository)
    turn_left_command_handler = TurnLeftCommandHandler(repo=repository)
    move_command_handler = MoveCommandHandler(repo=repository)

    return (InMemoryCommandDispatcherBuilder()
            .with_command_handler(TurnRight, turn_right_command_handler)
            .with_command_handler(TurnLeft, turn_left_command_handler)
            .with_command_handler(Move, move_command_handler)
            .with_projection(MarsRoverMoved, MarsRoverPathProjection(repo=repository, storage=storage))
            .build())


class MarsRoverExecutor:
    def __init__(self, repository: MarsRoverRepository, storage: List[Dict]):
        self.command_dispatcher: InMemoryCommandDispatcher = create_command_dispatcher(repository, storage)
        self.command_map = {"R": TurnRight(), "L": TurnLeft(), "M": Move()}

    def run(self, commands: str):
        parsed_commands = [self.command_map[c] for c in commands]

        for c in parsed_commands:
            self.command_dispatcher.submit(c)

        self.command_dispatcher.run()
