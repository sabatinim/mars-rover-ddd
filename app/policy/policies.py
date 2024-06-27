from app.command_handler.commands import NotifyObstacle, TurnOff
from app.ddd.basics import Policy, Command
from app.domain.events import ObstacleFound


class NotifyObstacleFoundPolicy(Policy):
    def apply(self, event: ObstacleFound) -> Command:
        return NotifyObstacle(message=f"Rover {event.id.value} hit obstacle")


class TurnOffPolicy(Policy):
    def apply(self, event: ObstacleFound) -> Command:
        return TurnOff(id=event.id)
