import dataclasses
import enum

from app.ddd.basics import Aggregate
from app.domain.direction import Direction
from app.domain.events import MarsRoverMoved, ObstacleFound, MarsRoverStarted, MarsRoverTurnedOff
from app.domain.mars_rover_id import MarsRoverId
from app.domain.point import Point
from app.domain.world import World


class MarsRoverStatus(enum.Enum):
    INITIALIZED = "INITIALIZED"
    STARTED = "STARTED"
    MOVING = "MOVING"
    OBSTACLE_FOUND = "OBSTACLE_FOUND"
    TURNED_OFF_FOR_AN_OBSTACLE = "TURNED_OFF"


@dataclasses.dataclass
class MarsRover(Aggregate):
    actual_point: Point
    direction: Direction
    world: World
    status: MarsRoverStatus | None

    def start(self) -> MarsRoverStarted:
        self.status = MarsRoverStatus.STARTED
        return MarsRoverStarted.create(self.id)

    def turn_right(self) -> MarsRoverMoved | None:
        if self._is_turned_off_for_an_obstacle():
            return None

        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.EAST
            case Direction.SOUTH:
                self.direction = Direction.WEST
            case Direction.WEST:
                self.direction = Direction.NORTH
            case Direction.EAST:
                self.direction = Direction.SOUTH
        self.status = MarsRoverStatus.MOVING
        return MarsRoverMoved.create(id=self.id)

    def turn_left(self) -> MarsRoverMoved | None:
        if self._is_turned_off_for_an_obstacle():
            return None

        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.WEST
            case Direction.SOUTH:
                self.direction = Direction.EAST
            case Direction.WEST:
                self.direction = Direction.SOUTH
            case Direction.EAST:
                self.direction = Direction.NORTH

        self.status = MarsRoverStatus.MOVING
        return MarsRoverMoved.create(id=self.id)

    def move(self) -> MarsRoverMoved | ObstacleFound | None:
        if self._is_turned_off_for_an_obstacle():
            return None

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
            self.status = MarsRoverStatus.OBSTACLE_FOUND
            return ObstacleFound.create(self.id)

        self.actual_point = next_point
        self.status = MarsRoverStatus.MOVING
        return MarsRoverMoved.create(id=self.id)

    def turn_off(self) -> MarsRoverTurnedOff:
        self.status = MarsRoverStatus.TURNED_OFF_FOR_AN_OBSTACLE
        return MarsRoverTurnedOff.create(self.id)

    def coordinate(self):
        hit_obstacles = "O:" if self._is_turned_off_for_an_obstacle() else ""

        return f"{hit_obstacles}{self.actual_point.x}:{self.actual_point.y}:{self.direction.value}"

    def _is_turned_off_for_an_obstacle(self):
        return self.status == MarsRoverStatus.TURNED_OFF_FOR_AN_OBSTACLE or self.status == MarsRoverStatus.OBSTACLE_FOUND

    @staticmethod
    def create(id: MarsRoverId, actual_point: Point, direction: Direction, world: World):
        return MarsRover(id=id,
                         version=0,
                         actual_point=actual_point,
                         world=world,
                         direction=direction,
                         status=MarsRoverStatus.INITIALIZED)
