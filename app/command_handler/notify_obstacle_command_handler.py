from app.command_handler.commands import NotifyObstacle
from app.ddd.basics import CommandHandler
from app.domain.events import ObstacleNotified


class NotifyObstacleCommandHandler(CommandHandler):
    def handle(self, command: NotifyObstacle) -> ObstacleNotified:
        print(command.message)
        return ObstacleNotified()
