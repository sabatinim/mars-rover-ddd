from copy import copy
from typing import Optional, Generic, TypeVar

from app.ddd.basics import Aggregate

AGGREGATE = TypeVar("AGGREGATE", bound=Aggregate)


class ConcurrencyException(Exception):
    pass


class InMemoryGenericAggregateRepository(Generic[AGGREGATE]):
    def __init__(self):
        self._resources = {}

    def save(self, computation):
        if self._resources.get(computation.id.value) and \
                self._resources[computation.id.value].version != computation.version:
            raise ConcurrencyException("Optimistic concurrency control check failed")

        self._resources[computation.id.value] = copy(computation)
        self._resources[computation.id.value].version += 1

    def get_by_id(self, request_id) -> Optional[Aggregate]:
        return self._resources.get(request_id.value)
