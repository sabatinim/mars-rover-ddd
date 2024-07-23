from typing import List, Dict

from app.ddd.basics import Projection
from app.domain.events import MarsRoverStarted
from app.domain.mars_rover import MarsRover
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository


class MarsRoverStartProjection(Projection):
    def __init__(self,
                 repo: InMemoryMarsRoverRepository,
                 mars_rover_path_view: List[Dict],
                 mars_rover_start_view: List[MarsRoverId]):
        self.repo = repo
        self.paths_storage = mars_rover_path_view
        self.mars_rover_storage = mars_rover_start_view

    def project(self, event: MarsRoverStarted):
        mars_rover: MarsRover = self.repo.get_by_id(event.id)

        raw = {"id": mars_rover.id.value, "actual_point": mars_rover.coordinate()}

        self.paths_storage.append(raw)
        self.mars_rover_storage.append(mars_rover.id.value)
