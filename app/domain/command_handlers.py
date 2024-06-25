from app.ddd.basics import CommandHandler
from app.ddd.command_dispatcher import InMemoryCommandDispatcherBuilder
from app.domain.commands import TurnRight, TurnLeft, Move
from app.domain.events import MarsRoverTurnedRight, MarsRoverTurnedLeft, MarsRoverMoved
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class TurnRightCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: TurnRight):
        mars_rover = self.repo.get_mars_rover()
        mars_rover.turn_right()

        self.repo.save(mars_rover)

        return MarsRoverTurnedRight()


class TurnLeftCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: TurnLeft):
        mars_rover = self.repo.get_mars_rover()
        mars_rover.turn_left()

        self.repo.save(mars_rover)

        return MarsRoverTurnedLeft()


class MoveCommandHandler(CommandHandler):
    def __init__(self, repo: MarsRoverRepository):
        self.repo = repo

    def handle(self, command: Move):
        mars_rover = self.repo.get_mars_rover()
        mars_rover.move()

        self.repo.save(mars_rover)

        return MarsRoverMoved()


def create_dispatcher_with(repository: MarsRoverRepository):
    turn_right_command_handler = TurnRightCommandHandler(repo=repository)
    turn_left_command_handler = TurnLeftCommandHandler(repo=repository)
    move_command_handler = MoveCommandHandler(repo=repository)

    return (InMemoryCommandDispatcherBuilder()
            .with_command_handler(TurnRight, turn_right_command_handler)
            .with_command_handler(TurnLeft, turn_left_command_handler)
            .with_command_handler(Move, move_command_handler)
            .build())


class MarsRoverExecutor:
    def __init__(self, repository: MarsRoverRepository):
        self.dispatcher = create_dispatcher_with(repository)
        self.command_map = {"R": TurnRight(), "L": TurnLeft(), "M": Move()}

    def run(self, commands):
        parsed_commands = [self.command_map[c] for c in commands]

        for c in parsed_commands:
            self.dispatcher.submit(c)

        self.dispatcher.run()
