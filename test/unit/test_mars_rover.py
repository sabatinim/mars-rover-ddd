import unittest

from app.domain.obstacles import Obstacles
from app.domain.point import Point
from app.factory import create_mars_rover


class TestMarsRover(unittest.TestCase):
    def test_turn_right(self):
        mars_rover = create_mars_rover()

        for c in ["0:0:E", "0:0:S", "0:0:W", "0:0:N"]:
            mars_rover.turn_right()
            self.assertEqual(c, mars_rover.coordinate())

    def test_turn_left(self):
        mars_rover = create_mars_rover()

        for c in ["0:0:W", "0:0:S", "0:0:E", "0:0:N"]:
            mars_rover.turn_left()
            self.assertEqual(c, mars_rover.coordinate())

    def test_grid_is_at_limit_on_x(self):
        mars_rover = create_mars_rover()

        mars_rover.turn_left()
        self.assertEqual("0:0:W", mars_rover.coordinate())

        for c in ["3:0:W", "2:0:W", "1:0:W", "0:0:W"]:
            mars_rover.move()
            self.assertEqual(c, mars_rover.coordinate())

        mars_rover.turn_right()
        self.assertEqual("0:0:N", mars_rover.coordinate(), )

    def test_grid_is_at_limit_on_y(self):
        mars_rover = create_mars_rover()
        for c in ["0:1:N", "0:2:N", "0:3:N", "0:0:N"]:
            mars_rover.move()
            self.assertEqual(c, mars_rover.coordinate())

    def test_hit_obstacle(self):
        mars_rover = create_mars_rover(obstacles=Obstacles.create(points=[Point.create(1, 1)]))
        mars_rover.turn_right()
        mars_rover.move()
        mars_rover.turn_left()
        mars_rover.move()
        mars_rover.move()
        mars_rover.move()
        mars_rover.turn_left()
        self.assertEqual("O:1:0:N", mars_rover.coordinate())
