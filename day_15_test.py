import unittest
from day_15 import Unit, Allegiace
from util import Coord


class TestDay15(unittest.TestCase):

    def test_nearest(self):
        origo = Unit(Allegiace.ELF, Coord(0, 0))
        closest = origo.closest([
            Coord(5, 5),
            Coord(-10, 3),
            Coord(6, 4),
            Coord(7, -4),
            Coord(-7, -2),
            Coord(6, 5),
        ],
            {
            Coord(0, 1): None,
            Coord(1, 0): None,
            Coord(-1, 0): None
        })

        self.assertEqual(closest, Coord(-7, -2))

        closest = origo.closest([
            Coord(5, 5),
            Coord(-10, 3),
            Coord(6, 4),
            Coord(7, -4),
            Coord(-7, -2),
            Coord(6, 5),
            Coord(1, 3)
        ],
            {
            Coord(0, 1): None,
            Coord(1, 0): None,
            Coord(-1, 0): None
        })
        self.assertEqual(closest, Coord(1, 3))

    def test_shortest_path_direction(self):
        origo = Coord(0, 0)
        other = Coord(4, 4)
        blocks1 = {
            Coord(0, 1),
            Coord(1, 1),
            Coord(1, 0),
            Coord(1, -1),
        }
        step = origo.shortest_path_direction(other, blocks1)
        self.assertEqual(step, Coord(-1, 0))

        blocks2 = {
            Coord(0, 1),
            Coord(1, 1),
            Coord(1, 0),
        }
        step = origo.shortest_path_direction(other, blocks2)
        self.assertEqual(step, Coord(0, -1))

        other2 = Coord(-4, -4)
        blocks2 = {
            Coord(0, -1),
            Coord(-1, -1),
            Coord(-1, 0),
        }
        step = origo.shortest_path_direction(other2, blocks2)
        self.assertEqual(step, Coord(1, 0))


if __name__ == '__main__':
    unittest.main(exit=False)
