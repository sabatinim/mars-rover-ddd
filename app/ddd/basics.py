import dataclasses
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
    pass


@dataclasses.dataclass
class Aggregate:
    id: AggregateId
    version: int


# class Policy:
#     async def apply(self, event):
#         pass
#
#
# class Projection:
#     async def project(self, event):
#         pass


class CommandHandler:
    async def handle(self, command: Command):
        pass
