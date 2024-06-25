import dataclasses
import json
from uuid import uuid4


class Command:
    pass


@dataclasses.dataclass(frozen=True)
class AggregateId:
    value: str

    @classmethod
    def new(cls):
        return cls(value=str(uuid4()))


class Event:
    def to_json(self):
        return json.dumps({"type": self.__class__.__name__,
                           **dataclasses.asdict(self)})


@dataclasses.dataclass
class Aggregate:
    id: AggregateId
    version: int


class Policy:
    async def apply(self, event):
        pass


class Projection:
    async def project(self, event):
        pass


class CommandHandler:
    async def handle(self, command: Command):
        pass


class StatusViolation(Exception):
    pass
