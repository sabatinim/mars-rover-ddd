from app.ddd.basics import CommandHandler
from app.domain.commands import Move
from app.domain.events import MarsRoverMoved
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class MoveCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: Move) -> MarsRoverMoved:
        mars_rover = self.repo.get_mars_rover()
        event = mars_rover.move()

        self.repo.save(mars_rover)

        return event
