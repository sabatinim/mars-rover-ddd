from app.factory import create_mars_rover, create_mars_rover_executor
from app.infrastructure.mars_rover_repository import MarsRoverRepository

if __name__ == "__main__":
    repository = MarsRoverRepository()
    repository.save(create_mars_rover())

    create_mars_rover_executor(repository=repository).run("RMLMM")

    actual = repository.get_mars_rover()
    print(actual.coordinate())
