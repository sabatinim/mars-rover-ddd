from app.command_handler.commands import NotifyObstacleHit
from app.ddd.basics import Policy, Command
from app.domain.events import ObstacleHit


class NotifyObstacleHitPolicy(Policy):
    def apply(self, event: ObstacleHit) -> Command:
        return NotifyObstacleHit(message=f"Rover {event.id.value} hit obstacle")
