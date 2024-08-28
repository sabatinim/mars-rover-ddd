from app.ddd.basics import CommandHandler
from app.command_handler.commands import TurnRight
from app.domain.events import MarsRoverMoved, ObstacleHit
from app.domain.mars_rover import MarsRover
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository


class TurnRightCommandHandler(CommandHandler):
    def __init__(self, repo: InMemoryMarsRoverRepository):
        self.repo = repo

    def handle(self, command: TurnRight) -> ObstacleHit | MarsRoverMoved:
        mars_rover: MarsRover = self.repo.get_by_id(command.id)
        event = mars_rover.turn_right()
        self.repo.save(mars_rover)

        return event
