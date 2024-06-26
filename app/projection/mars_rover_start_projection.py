from typing import List, Dict

from app.ddd.basics import Projection
from app.domain.events import MarsRoverStarted
from app.domain.mars_rover import MarsRover
from app.infrastructure.mars_rover_repository import MarsRoverRepository


class MarsRoverStartProjection(Projection):
    def __init__(self, repo: MarsRoverRepository, storage: List[Dict]):
        self.repo = repo
        self.storage = storage

    def project(self, event: MarsRoverStarted):
        mars_rover: MarsRover = self.repo.get_by_id(event.id)

        raw = {"id": mars_rover.id.value, "actual_point": mars_rover.coordinate()}

        self.storage.append(raw)
