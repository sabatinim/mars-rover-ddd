from app.ddd.generic_aggregate_repository import InMemoryGenericAggregateRepository
from app.domain.mars_rover import MarsRover


class MarsRoverRepository(InMemoryGenericAggregateRepository[MarsRover]):
    def get_mars_rover(self) -> MarsRover:
        return list(self._resources.values())[0]
