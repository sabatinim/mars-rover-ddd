from typing import List, Dict, Type

from app.ddd.basics import Command, CommandHandler, Projection, Policy, Event


class InMemoryCommandDispatcher:
    def __init__(self,
                 command_handlers: Dict[Type[Command], CommandHandler],
                 projections: Dict[Type[Event], List[Projection]],
                 policies: Dict[Type[Event], List[Policy]]):
        self.command_handlers = command_handlers
        self.projections = projections
        self.policies = policies

        self.commands: List[Command] = []

    def submit(self, command: Command):
        self.commands.append(command)
        return self

    def run(self):
        while self.commands:
            command = self.commands.pop(0)
            print(f"[COMMAND] {command}")

            event: Event = self.command_handlers[type(command)].handle(command)
            print(f"[EVENT] {event}")

            event_policies = self.policies.get(type(event), [])
            for policy in event_policies:
                new_command = policy.apply(event)
                if new_command:
                    self.commands.append(new_command)

            for projection in self.projections.get(type(event), []):
                projection.project(event)
