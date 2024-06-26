from app.ddd.generic_aggregate_repository import InMemoryGenericAggregateRepository
from app.domain.mars_rover import MarsRover


class MarsRoverRepository(InMemoryGenericAggregateRepository[MarsRover]):
    pass
