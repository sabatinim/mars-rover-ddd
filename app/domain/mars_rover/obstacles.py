import dataclasses
from typing import List

from app.domain.mars_rover.point import Point


@dataclasses.dataclass
class Obstacles:
    points: List[Point]

    @staticmethod
    def create(points: List[Point]) -> 'Obstacles':
        return Obstacles(points=points)
