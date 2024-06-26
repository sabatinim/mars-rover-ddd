from app.domain.mars_rover_id import MarsRoverId
from app.factory import create_mars_rover_executor, create_mars_rover_starter
from app.infrastructure.mars_rover_repository import MarsRoverRepository
from app.service.mars_rover_executor import MarsRoverRunner
from app.service.mars_rover_starter import MarsRoverStarter

if __name__ == "__main__":
    repository = MarsRoverRepository()
    projections_storage = []

    starter: MarsRoverStarter = create_mars_rover_starter(repository=repository, storage=projections_storage)
    starter.start()
    starter.start()

    id1 = projections_storage[0].get("id")
    id2 = projections_storage[1].get("id")

    runner: MarsRoverRunner = create_mars_rover_executor(repository=repository, storage=projections_storage)

    runner.run(id1, "RMMLMMMMLMMM")
    runner.run(id2, "RMMRM")

    first = repository.get_by_id(MarsRoverId(id1))
    second = repository.get_by_id(MarsRoverId(id2))
    print(f"Actual Mars Rover Coordinate {id1}: {first.coordinate()}")
    print(f"Actual Mars Rover Coordinate {id2}: {second.coordinate()}")

    for s in sorted(projections_storage, key=lambda i:i["id"]):
        print(s)
