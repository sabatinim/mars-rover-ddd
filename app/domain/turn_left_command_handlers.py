from app.ddd.basics import CommandHandler
from app.domain.commands import TurnLeft
from app.domain.events import MarsRoverMoved
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class TurnLeftCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: TurnLeft) -> MarsRoverMoved:
        mars_rover = self.repo.get_mars_rover()
        event = mars_rover.turn_left()

        self.repo.save(mars_rover)

        return event
