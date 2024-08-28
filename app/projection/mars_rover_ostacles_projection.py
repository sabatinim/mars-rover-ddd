from typing import Set, Tuple

from app.ddd.basics import Projection
from app.domain.events import ObstacleHit


class MarsRoverObstaclesProjection(Projection):
    def __init__(self, obstacle_view: Set[Tuple[int, int]]):
        self.storage = obstacle_view

    def project(self, event: ObstacleHit):
        self.storage.add(event.coordinate)
