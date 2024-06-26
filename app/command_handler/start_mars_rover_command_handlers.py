from app.ddd.basics import CommandHandler
from app.command_handler.commands import StartMarsRover
from app.domain.events import MarsRoverStarted
from app.domain.mars_rover import MarsRover
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class StartMarsRoverCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: StartMarsRover) -> MarsRoverStarted:
        mars_rover: MarsRover = MarsRover.create(id=MarsRoverId.new(),
                                                 actual_point=command.initial_point,
                                                 direction=command.initial_direction,
                                                 world=command.world)
        event = mars_rover.start()
        self.repo.save(mars_rover)

        return event
