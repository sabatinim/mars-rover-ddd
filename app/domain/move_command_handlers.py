from app.ddd.basics import CommandHandler
from app.domain.commands import Move
from app.domain.events import MarsRoverMoved
from app.domain.mars_rover.mars_rover import MarsRover
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class MoveCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: Move) -> MarsRoverMoved:
        mars_rover: MarsRover = self.repo.get_by_id(command.id)
        event = mars_rover.move()

        self.repo.save(mars_rover)

        return event
