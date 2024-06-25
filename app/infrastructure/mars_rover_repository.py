from app.ddd.generic_aggregate_repository import InMemoryGenericAggregateRepository
from app.domain.mars_rover import MarsRoverAgg


class MarsRoverRepository(InMemoryGenericAggregateRepository[MarsRoverAgg]):
    def get_mars_rover(self) -> MarsRoverAgg:
        return list(self._resources.values())[0]
