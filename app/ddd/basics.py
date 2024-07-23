import dataclasses
from uuid import uuid4


class Command:
    pass


class Event:
    pass


@dataclasses.dataclass(frozen=True)
class AggregateId:
    value: str

    @classmethod
    def new(cls):
        return cls(value=str(uuid4()))


@dataclasses.dataclass
class Aggregate:
    id: AggregateId
    version: int


class CommandHandler:
    def handle(self, command: Command) -> Event:
        pass


class Policy:
    def apply(self, event: Event) -> Command:
        pass


class Projection:
    def project(self, event: Event):
        pass
