import unittest

from app.domain.mars_rover import Direction, Point
from test.factory import create_mars_rover_agg


class TestMarsRover(unittest.TestCase):
    def test_turn_right(self):
        mars_rover = create_mars_rover_agg()

        mars_rover.turn_right()

        self.assertEqual(mars_rover.coordinate(), "0:0:E")

    def test_turn_left(self):
        mars_rover = create_mars_rover_agg()

        mars_rover.turn_left()

        self.assertEqual(mars_rover.coordinate(), "0:0:W")

    def test_move_on_x(self):
        mars_rover = create_mars_rover_agg(actual_point=Point.create(0, 0), direction=Direction.EAST)
        mars_rover.move()
        mars_rover.move()

        self.assertEqual(mars_rover.coordinate(), "2:0:E")

    def test_move_on_y(self):
        mars_rover = create_mars_rover_agg(actual_point=Point.create(0, 0), direction=Direction.WEST)
        mars_rover.move()
        mars_rover.move()

        self.assertEqual(mars_rover.coordinate(), "2:0:W")
