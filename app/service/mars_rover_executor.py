from typing import List, Dict

from app.ddd.command_dispatcher import InMemoryCommandDispatcher
from app.command_handler.commands import TurnRight, TurnLeft, Move
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.workflow_factory import create_command_dispatcher


class MarsRoverRunner:
    def __init__(self, repository: MarsRoverRepository, storage: List[Dict]):
        self.command_dispatcher: InMemoryCommandDispatcher = create_command_dispatcher(repository, storage)
        self.command_map = {"R": TurnRight, "L": TurnLeft, "M": Move}

    def run(self, rover_id: str, commands: str):
        parsed_commands = [self.command_map[c](MarsRoverId(rover_id)) for c in commands]

        self.command_dispatcher.submit(commands=parsed_commands)

        self.command_dispatcher.run()
