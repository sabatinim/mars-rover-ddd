from typing import Dict, Type, List

from app.ddd.basics import Command, CommandHandler, Event, Projection, Policy
from app.ddd.command_dispatcher import InMemoryCommandDispatcher


class InMemoryCommandDispatcherBuilder:
    def __init__(self):
        self.command_handlers: Dict[Type[Command], CommandHandler] = {}
        self.projections: Dict[Type[Event], List[Projection]] = {}
        self.policies: Dict[Type[Event], List[Policy]] = {}

    def with_command_handler(self, command_type: Type[Command], command_handler: CommandHandler):
        self.command_handlers[command_type] = command_handler
        return self

    def with_policy(self, event_type, policy):
        if event_type not in self.policies:
            self.policies[event_type] = []

        self.policies[event_type].append(policy)
        return self

    def with_projection(self, event_type, projection):
        if event_type not in self.projections:
            self.projections[event_type] = []
        self.projections[event_type].append(projection)
        return self

    def build(self) -> InMemoryCommandDispatcher:
        return InMemoryCommandDispatcher(command_handlers=self.command_handlers,
                                         projections=self.projections,
                                         policies=self.policies)
