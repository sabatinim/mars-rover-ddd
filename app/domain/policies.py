from app.ddd.basics import Policy, Command
from app.domain.commands import NotifyObstacle
from app.domain.events import ObstacleFound


class ObstacleFoundPolicy(Policy):
    def apply(self, event:ObstacleFound) -> Command:
        return NotifyObstacle(message=f"Rover {event.id.value} hit obstacle")