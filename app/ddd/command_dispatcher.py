from typing import List, Dict, Type

from app.ddd.basics import Command, CommandHandler, Projection, Policy, Event


class InMemoryCommandDispatcher:
    def __init__(self,
                 command_handlers: Dict[Type[Command], CommandHandler],
                 projections: Dict[Type[Event], Projection],
                 policies: Dict[Type[Event], Policy]):
        self.command_handlers = command_handlers
        self.projections = projections
        self.policies = policies

        self.commands: List[Command] = []

    def submit(self, command: Command):
        self.commands.append(command)

    def run(self):
        while self.commands:
            command = self.commands.pop(0)
            print(f"[COMMAND] {command}")

            event: Event = self.command_handlers[type(command)].handle(command)

            print(f"[EVENT] {event} generated")
            event_policies = self.policies.get(type(event), [])
            for policy in event_policies:
                new_command = policy.apply(event)
                if new_command:
                    self.commands.append(new_command)

            for projection in self.projections.get(type(event), []):
                projection.project(event)


class InMemoryCommandDispatcherBuilder:
    def __init__(self):
        self.command_handlers: Dict[Type[Command], CommandHandler] = {}
        self.projections: Dict[Type[Event], Projection] = {}
        self.policies: Dict[Type[Event], Policy] = {}

    def with_command_handler(self, command_type: Type[Command], command_handler: CommandHandler):
        self.command_handlers[command_type] = command_handler
        return self

    # def with_policy(self, event_type, policy):
    #     if event_type not in self._policies:
    #         self._policies[event_type] = []
    #
    #     self._policies[event_type].append(policy)
    #     return self
    #
    # def with_projection(self, event_type, projection):
    #     if event_type not in self._projections:
    #         self._projections[event_type] = []
    #     self._projections[event_type].append(projection)
    #     return self

    def build(self) -> InMemoryCommandDispatcher:
        return InMemoryCommandDispatcher(command_handlers=self.command_handlers,
                                         projections=self.projections,
                                         policies=self.policies)
