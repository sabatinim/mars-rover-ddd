from app.factory import create_mars_rover, create_mars_rover_executor
from app.infrastructure.mars_rover_repository import MarsRoverRepository

if __name__ == "__main__":
    repository = MarsRoverRepository()
    mars_rover = create_mars_rover()
    repository.save(mars_rover)
    storage = [{"id": mars_rover.id.value,
                "actual_point": mars_rover.coordinate()}]

    create_mars_rover_executor(repository=repository,
                               storage=storage).run("RMLMM")

    actual = repository.get_mars_rover()
    print(actual.coordinate())
    for s in storage:
        print(s)
