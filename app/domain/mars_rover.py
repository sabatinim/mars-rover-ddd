import dataclasses
import enum

from app.ddd.basics import Aggregate
from app.domain.direction import Direction
from app.domain.events import MarsRoverMoved, ObstacleHit, MarsRoverStarted, MarsRoverTurnedOff
from app.domain.mars_rover_id import MarsRoverId
from app.domain.point import Point
from app.domain.world import World


class MarsRoverStatus(enum.Enum):
    CREATED = "CREATED"
    STARTED = "STARTED"
    MOVED = "MOVED"
    OBSTACLE_HIT = "OBSTACLE_HIT"
    TURNED_OFF = "TURNED_OFF"


@dataclasses.dataclass
class MarsRover(Aggregate):
    actual_point: Point
    direction: Direction
    world: World
    status: MarsRoverStatus

    def start(self) -> MarsRoverStarted:
        self.status = MarsRoverStatus.STARTED
        return MarsRoverStarted.create(self.id)

    def turn_right(self) -> MarsRoverMoved | MarsRoverTurnedOff:
        if self._is_turned_off():
            return MarsRoverTurnedOff.create(self.id)

        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.EAST
            case Direction.SOUTH:
                self.direction = Direction.WEST
            case Direction.WEST:
                self.direction = Direction.NORTH
            case Direction.EAST:
                self.direction = Direction.SOUTH

        self.status = MarsRoverStatus.MOVED
        return MarsRoverMoved.create(id=self.id)

    def turn_left(self) -> MarsRoverMoved | MarsRoverTurnedOff:
        if self._is_turned_off():
            return MarsRoverTurnedOff.create(self.id)

        match self.direction:
            case Direction.NORTH:
                self.direction = Direction.WEST
            case Direction.SOUTH:
                self.direction = Direction.EAST
            case Direction.WEST:
                self.direction = Direction.SOUTH
            case Direction.EAST:
                self.direction = Direction.NORTH

        self.status = MarsRoverStatus.MOVED
        return MarsRoverMoved.create(id=self.id)

    def move(self) -> MarsRoverMoved | ObstacleHit | MarsRoverTurnedOff:
        if self._is_turned_off():
            return MarsRoverTurnedOff.create(self.id)

        rover_x = self.actual_point.x
        rover_y = self.actual_point.y

        world_x = self.world.x()
        world_y = self.world.y()

        match self.direction:
            case Direction.NORTH:
                next_y = (rover_y + 1) % world_y
                next_point = Point.create(rover_x, next_y)

            case Direction.SOUTH:
                next_y = (rover_y - 1) % world_y
                next_point = Point.create(rover_x, next_y)

            case Direction.WEST:
                next_x = (rover_x - 1) % world_x
                next_point = Point.create(next_x, rover_y)

            case Direction.EAST:
                next_x = (rover_x + 1) % world_x
                next_point = Point.create(next_x, rover_y)

        if self.world.hit_obstacles(next_point):
            self.status = MarsRoverStatus.OBSTACLE_HIT
            return ObstacleHit.create(id=self.id, coordinate=(next_point.x, next_point.y))
        else:
            self.actual_point = next_point
            self.status = MarsRoverStatus.MOVED
            return MarsRoverMoved.create(id=self.id)

    def turn_off(self) -> MarsRoverTurnedOff:
        self.status = MarsRoverStatus.TURNED_OFF
        return MarsRoverTurnedOff.create(id=self.id)

    def coordinate(self):
        hit_obstacles = "O:" if self._is_obstacle_hit() or self._is_turned_off() else ""

        return f"{hit_obstacles}{self.actual_point.x}:{self.actual_point.y}:{self.direction.value}"

    def _is_turned_off(self):
        return MarsRoverStatus.TURNED_OFF == self.status

    def _is_obstacle_hit(self):
        return self.status == MarsRoverStatus.OBSTACLE_HIT

    @staticmethod
    def create(id: MarsRoverId, actual_point: Point, direction: Direction, world: World):
        return MarsRover(id=id,
                         version=0,
                         actual_point=actual_point,
                         world=world,
                         direction=direction,
                         status=MarsRoverStatus.CREATED)
