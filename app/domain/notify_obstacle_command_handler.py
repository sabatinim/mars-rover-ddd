from app.ddd.basics import CommandHandler, Event
from app.domain.commands import NotifyObstacle
from app.domain.events import ObstacleNotified


class NotifyObstacleCommandHandler(CommandHandler):
    def handle(self, command: NotifyObstacle) -> Event:
        print(command.message)
        return ObstacleNotified()
