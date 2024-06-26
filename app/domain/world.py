import dataclasses
from typing import Tuple

from app.domain.obstacles import Obstacles
from app.domain.point import Point


@dataclasses.dataclass
class World:
    dimension: Tuple[int, int]
    obstacles: Obstacles

    def hit_obstacles(self, point: Point):
        for p in self.obstacles.points:
            if p == point:
                return True
        return False

    @staticmethod
    def create(dimension: Tuple[int, int], obstacles: Obstacles):
        return World(dimension=dimension, obstacles=obstacles)
