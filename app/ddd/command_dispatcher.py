from app.ddd.basics import Command, Event


class InMemoryCommandDispatcher:
    def __init__(self, command_handler: dict, projections: dict, policies: dict):
        self._command_queue = []
        self._command_handler = command_handler
        self._projections = projections
        self._policies = policies

    def submit(self, command: Command):
        self._command_queue.append(command)

    def run(self):
        while self._command_queue:
            command = self._command_queue.pop(0)
            print(f"[COMMAND] {command}")

            event = self._command_handler[type(command)].handle(command)

            self.process_event(event)

    def process_event(self, event: Event):
        print(f"[EVENT] {event} generated")
        event_policies = self._policies.get(type(event), [])
        for policy in event_policies:
            new_command = policy.apply(event)
            if new_command:
                self._command_queue.append(new_command)

        for projection in self._projections.get(type(event), []):
            projection.project(event)


class InMemoryCommandDispatcherBuilder:
    def __init__(self):
        self._command_handler = {}
        self._projections = {}
        self._policies = {}

    def with_command_handler(self, command_type, command_handler):
        self._command_handler[command_type] = command_handler
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
        return InMemoryCommandDispatcher(self._command_handler, self._projections, self._policies)
