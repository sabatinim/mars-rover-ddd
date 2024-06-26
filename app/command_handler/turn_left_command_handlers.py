from app.ddd.basics import CommandHandler
from app.command_handler.commands import TurnLeft
from app.domain.events import MarsRoverMoved
from app.domain.mars_rover import MarsRover
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class TurnLeftCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: TurnLeft) -> MarsRoverMoved:
        mars_rover: MarsRover = self.repo.get_by_id(command.id)
        event = mars_rover.turn_left()
        self.repo.save(mars_rover)

        return event
