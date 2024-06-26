import dataclasses
import enum

from app.ddd.basics import Aggregate
from app.domain.events import MarsRoverMoved, ObstacleFound
from app.domain.mars_rover.direction import Direction
from app.domain.mars_rover.mars_rover_id import MarsRoverId
from app.domain.mars_rover.point import Point
from app.domain.mars_rover.world import World


class MarsRoverStatus(enum.Enum):
    NO_OBSTACLES = "NO_OBSTACLES"
    OBSTACLES = "OBSTACLES"


@dataclasses.dataclass
class MarsRover(Aggregate):
    actual_point: Point
    direction: Direction
    world: World
    status: MarsRoverStatus = MarsRoverStatus.NO_OBSTACLES

    def turn_right(self) -> MarsRoverMoved:
        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.EAST
            case Direction.SOUTH:
                self.direction = Direction.WEST
            case Direction.WEST:
                self.direction = Direction.NORTH
            case Direction.EAST:
                self.direction = Direction.SOUTH

        return MarsRoverMoved.create(id=self.id)

    def turn_left(self) -> MarsRoverMoved:
        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.WEST
            case Direction.SOUTH:
                self.direction = Direction.EAST
            case Direction.WEST:
                self.direction = Direction.SOUTH
            case Direction.EAST:
                self.direction = Direction.NORTH

        return MarsRoverMoved.create(id=self.id)

    def move(self) -> MarsRoverMoved | ObstacleFound:
        match self.direction:
            case Direction.NORTH:
                next_y = (self.actual_point.y + 1) % self.world.dimension[1]
                next_point = Point.create(self.actual_point.x, next_y)

            case Direction.SOUTH:
                next_y = (self.actual_point.y - 1) % self.world.dimension[1]
                next_point = Point.create(self.actual_point.x, next_y)

            case Direction.WEST:
                next_x = (self.actual_point.x - 1) % self.world.dimension[0]
                next_point = Point.create(next_x, self.actual_point.y)

            case Direction.EAST:
                next_x = (self.actual_point.x + 1) % self.world.dimension[0]
                next_point = Point.create(next_x, self.actual_point.y)

        if self.world.hit_obstacles(next_point):
            self.status = MarsRoverStatus.OBSTACLES
            return ObstacleFound.create(self.id)

        self.actual_point = next_point

        return MarsRoverMoved.create(id=self.id)

    def coordinate(self):
        hit_obstacles = "O:" if self.status == MarsRoverStatus.OBSTACLES else ""

        return f"{hit_obstacles}{self.actual_point.x}:{self.actual_point.y}:{self.direction.value}"

    @staticmethod
    def create(id: MarsRoverId, actual_point: Point, direction: Direction, world: World):
        return MarsRover(id=id,
                         version=0,
                         actual_point=actual_point,
                         world=world,
                         direction=direction)