import random
from collections import defaultdict

from app.domain.direction import Direction
from app.domain.mars_rover_id import MarsRoverId
from app.infrastructure.mars_rover_repository import MarsRoverRepository
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
    repository = MarsRoverRepository()
    paths = []
    obstacles = []

    runner = (
        MarsRoverRunner(repository=repository,
                        path_projection_storage=paths,
                        obstacles_projection_storage=obstacles)
        .with_initial_point(x=0, y=0)
        .with_initial_direction(direction=Direction.NORTH)
        .with_world(world_dimension=(4, 4), obstacles=[(2, 2)])
    )

    ids = []
    number_of_rovers = 2
    for i in range(number_of_rovers):
        runner.start()
        ids.append(paths[i].get("id"))

    commands = {}
    for i in ids:
        random_commands = generate_random_commands(3)
        commands[i] = random_commands
        runner.run(i, random_commands)

    grouped_paths = group_by(paths)
    grouped_obstacles = group_by(obstacles)

    for k, v in grouped_paths.items():
        print(f"##### {k} #####")
        first = repository.get_by_id(MarsRoverId(k))
        print(f"Commands: {commands.get(k)}")
        print(f"Actual Coordinate: {first.coordinate()}")
        print(f"Paths: {v}")
        print(f"Obstacles: {grouped_obstacles.get(k, [])}")
