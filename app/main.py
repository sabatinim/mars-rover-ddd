import random
from collections import defaultdict

from app.domain.direction import Direction
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import InMemoryMarsRoverRepository
from app.service.mars_rover_runner import MarsRoverRunner


def generate_random_commands(length):
    possible_chars = 'MRL'
    random_string = ''.join(random.choice(possible_chars) for _ in range(length))
    return random_string


def group_by(storage):
    sorted_storage = sorted(storage, key=lambda i: i["id"])
    storage_as_tuple = [(p["id"], p.get("actual_point") or p.get("obstacle")) for p in sorted_storage]
    grouped_storage = defaultdict(list)
    for key, value in storage_as_tuple:
        grouped_storage[key].append(value)
    return grouped_storage


if __name__ == "__main__":
    number_of_rovers = 12
    commands_length = 600
    world_dimension = (10, 10)
    world_obstacles = [(1, 2), (1, 1), (4, 6), (5, 9), (5, 5)]

    repository = InMemoryMarsRoverRepository()
    paths_table = []
    obstacles_table = set()
    mars_rover_ids_table = []

    runner = (
        MarsRoverRunner(repository=repository,
                        mars_rover_path_view=paths_table,
                        obstacle_view=obstacles_table,
                        mars_rover_start_view=mars_rover_ids_table)
        .with_initial_point(x=0, y=0)
        .with_initial_direction(direction=Direction.NORTH)
        .with_world(world_dimension=world_dimension, obstacles=world_obstacles)
    )

    commands = {}
    for i in range(number_of_rovers):
        runner.start_rover()
        id = mars_rover_ids_table[i]

        random_commands = generate_random_commands(commands_length)
        commands[id] = random_commands

        runner.execute(id.value, commands[id])

    grouped_paths = group_by(paths_table)

    for id in mars_rover_ids_table:
        print(f"################################################################################")
        print(f"RoverId: {id}")
        mars_rover = repository.get_by_id(id)
        print(f"Commands: {commands.get(id)}")
        print(f"Actual Coordinate: {mars_rover.coordinate()}")
        print(f"Paths: {grouped_paths.get(id.value)}, length: {len(grouped_paths.get(id.value))}")
        print(f"Obstacles: {obstacles_table}")
