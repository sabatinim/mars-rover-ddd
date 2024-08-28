from app.command_handler.commands import NotifyObstacleHit
from app.ddd.basics import CommandHandler
from app.domain.events import ObstacleNotified


class NotifyObstacleCommandHandler(CommandHandler):
    def handle(self, command: NotifyObstacleHit) -> ObstacleNotified:
        print(command.message)
        return ObstacleNotified()
