from app.command_handler.commands import TurnOff
from app.ddd.basics import CommandHandler
from app.domain.events import MarsRoverTurnedOff
from app.domain.mars_rover import MarsRover
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository


class TurnOffCommandHandler(CommandHandler):
    def __init__(self, repo: InMemoryMarsRoverRepository):
        self.repo = repo

    def handle(self, command: TurnOff) -> MarsRoverTurnedOff:
        mars_rover: MarsRover = self.repo.get_by_id(command.id)
        event = mars_rover.turn_off()
        self.repo.save(mars_rover)

        return event
