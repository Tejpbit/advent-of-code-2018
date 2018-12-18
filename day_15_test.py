import unittest
from day_15 import Unit, Allegiace, part1
from util import Coord


class TestDay15(unittest.TestCase):

    # def test_nearest(self):
    #     origo = Unit(Allegiace.ELF, Coord(0, 0))
    #     closest = origo.closest([
    #         Coord(5, 5),
    #         Coord(-10, 3),
    #         Coord(6, 4),
    #         Coord(7, -4),
    #         Coord(-7, -2),
    #         Coord(6, 5),
    #     ],
    #         {
    #         Coord(0, 1): None,
    #         Coord(1, 0): None,
    #         Coord(-1, 0): None
    #     })

    #     self.assertEqual(closest, Coord(-7, -2))

    #     closest = origo.closest([
    #         Coord(5, 5),
    #         Coord(-10, 3),
    #         Coord(6, 4),
    #         Coord(7, -4),
    #         Coord(-7, -2),
    #         Coord(6, 5),
    #         Coord(1, 3)
    #     ],
    #         {
    #         Coord(0, 1): None,
    #         Coord(1, 0): None,
    #         Coord(-1, 0): None
    #     })
    #     self.assertEqual(closest, Coord(1, 3))

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

    def exampels_extract_result(self, game):
        rounds = game.round_count
        hit_point_sum = sum(map(lambda u: u.hit_points, game.units))
        return (rounds, hit_point_sum)

    def exampel_test(self, example_file, expected_rounds, expected_summarized_hp, expected_end_pretty=None):
        game = part1(example_file)

        if expected_end_pretty:
            print("Compare")
            print(expected_end_pretty)
            print(game.pretty_str())
            print(game.pretty_healthstats())
            self.assertEqual(game.pretty_str(), expected_end_pretty)

        res = self.exampels_extract_result(game)
        self.assertEqual(res[0], expected_rounds)
        self.assertEqual(res[1], expected_summarized_hp)

    def test_examples(self):
        self.exampel_test("day_15.example1.data", 37, 982)
        self.exampel_test("day_15.example2.data", 46, 859)
        self.exampel_test("day_15.example3.data", 35, 793)
        self.exampel_test("day_15.example4.data", 54, 536)
        self.exampel_test("day_15.example5.data", 20, 937)


if __name__ == '__main__':
    unittest.main(exit=False)
