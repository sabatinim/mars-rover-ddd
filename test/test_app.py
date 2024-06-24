import unittest

from app.domain.commands import Direction, Point
from app.factory import create_mars_rover


class TestApp(unittest.TestCase):
    def test_turn_right(self):
        actual = create_mars_rover().run("R")

        self.assertEqual(actual, "0:0:E")

    def test_turn_left(self):
        actual = create_mars_rover().run("L")

        self.assertEqual(actual, "0:0:W")

    def test_move(self):
        actual = create_mars_rover().run("M")

        self.assertEqual(actual, "0:1:N")

    def test_move_double(self):
        actual = create_mars_rover().run("MM")

        self.assertEqual(actual, "0:2:N")

    def test_move_on_x(self):
        actual = create_mars_rover(actual_point=Point(0, 0, Direction.EAST)).run("MM")

        self.assertEqual(actual, "2:0:E")

    def test_move_on_y(self):
        actual = create_mars_rover(actual_point=Point(0, 0, Direction.WEST)).run("MM")

        self.assertEqual(actual, "2:0:W")
