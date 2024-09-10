from app.command_handler.commands import NotifyObstacleHit, TurnOff
from app.ddd.basics import Policy, Command
from app.domain.events import ObstacleHit


class TurnOffObstacleHitPolicy(Policy):
    def apply(self, event: ObstacleHit) -> Command:
        return TurnOff(id=event.id)


class NotifyObstacleHitPolicy(Policy):
    def apply(self, event: ObstacleHit) -> Command:
        return NotifyObstacleHit(message=f"Rover {event.id.value} hit obstacle")
