import unittest

from test.factory import create_mars_rover_agg


class TestMarsRover(unittest.TestCase):
    def test_turn_right(self):
        mars_rover = create_mars_rover_agg()

        for c in ["0:0:E", "0:0:S", "0:0:W", "0:0:N"]:
            mars_rover.turn_right()
            self.assertEqual(mars_rover.coordinate(), c)

    def test_turn_left(self):
        mars_rover = create_mars_rover_agg()

        for c in ["0:0:W", "0:0:S", "0:0:E", "0:0:N"]:
            mars_rover.turn_left()
            self.assertEqual(mars_rover.coordinate(), c)

    def test_grid_is_at_limit_on_x(self):
        mars_rover = create_mars_rover_agg()

        mars_rover.turn_left()
        self.assertEqual(mars_rover.coordinate(), "0:0:W")

        for c in ["3:0:W", "2:0:W", "1:0:W", "0:0:W"]:
            mars_rover.move()
            self.assertEqual(mars_rover.coordinate(), c)

        mars_rover.turn_right()
        self.assertEqual(mars_rover.coordinate(), "0:0:N")

    def test_grid_is_at_limit_on_y(self):
        mars_rover = create_mars_rover_agg()
        for c in ["0:1:N", "0:2:N", "0:3:N", "0:0:N"]:
            mars_rover.move()
            self.assertEqual(mars_rover.coordinate(), c)


