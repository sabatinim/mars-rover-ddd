from typing import List, Dict

from app.ddd.basics import Projection
from app.domain.events import ObstacleFound


class MarsRoverObstaclesProjection(Projection):
    def __init__(self, storage: List[Dict]):
        self.storage = storage

    def project(self, event: ObstacleFound):
        raw = {"id": event.id.value, "obstacle": event.coordinate}

        self.storage.append(raw)
