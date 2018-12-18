from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set  # , OrderedDict
import functools
import collections
import math

from util import Coord, red, bold

from enum import Enum


class Allegiace(Enum):
    GOBLIN = "G"
    ELF = "E"


class Wall:

    def __repr__(self):
        return '#'


WALL = Wall()


@dataclass
class Unit:
    allegiance: Allegiace
    position: Coord
    attack_power = 3
    hit_points = 200

    def turn(self):
        pass

    def attack(self, target: "Unit"):
        pass

    def distance_to(self, coord: Coord):
        return self.position.manhattanDistance(coord)

    def move(self, direction: Coord):
        self.position = self.position.moveByCoord(direction)


def parse(file):
    board: Dict[Coord, any] = dict()
    units: List[Unit] = []

    lines = file.readlines()
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == "#":
                board[Coord(x, y)] = WALL
            elif cell == ".":
                pass
            elif cell == "G":
                #units[Coord(x, y)] = Unit(Allegiace.GOBLIN, Coord(x, y))
                units.append(Unit(Allegiace.GOBLIN, Coord(x, y)))
            elif cell == "E":
                #units[Coord(x, y)] = Unit(Allegiace.ELF, Coord(x, y))
                units.append(Unit(Allegiace.ELF, Coord(x, y)))
            elif cell == "\n":
                pass
            else:
                exit("Invalid input")
    return Game(board, units)


@dataclass
class Game:
    board: Dict[Coord, any]
    units: List[Unit]
    round_count: int
    attacks_this_round: List[Unit]
    moves_this_round: List[Unit]

    def __init__(self, board, units):
        self.board = board
        self.units = sorted(units, key=lambda unit: unit.position)
        self.round_count = 0
        self.attacks_this_round = []
        self.moves_this_round = []

    def setElvesAttackPower(self, attack_power: int):
        for u in self.units:
            if u.allegiance == Allegiace.ELF:
                u.attack_power = attack_power

    def targets(self, unit: Unit):
        units_of_opposite_faction = list(
            filter(lambda other_unit: unit.allegiance is not other_unit.allegiance, self.units))
        return units_of_opposite_faction

    def open_squares(self, unit):
        neighborCoords = unit.position.manhattanNeighbours()
        open_squares = set()
        for coord in neighborCoords:
            if coord not in self.board:
                open_squares.add(coord)
        return open_squares

    def other_units(self, unit: Unit):
        other_units = self.units.copy()
        other_units.remove(unit)
        return other_units

    def closest(self, unit: Unit, coords: List[Coord]):
        if unit.position in coords:
            return unit.position
        targets = set(coords)
        positionsHistory: Set(Coord) = set()

        positionsHistory = set()
        positionsHistory.add(unit.position)
        newPositions = positionsHistory

        while True:
            newPositions = set().union(
                *[pos.manhattanNeighbours() for pos in newPositions])
            newPositions.difference_update(positionsHistory)
            newPositions.difference_update(set(self.board.keys()))
            newPositions.difference_update(
                set(map(lambda u: u.position, self.other_units(unit))))

            if newPositions.__len__() == 0:
                break

            if not targets.isdisjoint(newPositions):
                closest = targets.intersection(newPositions)
                closest = list(closest)
                closest.sort()
                return closest[0]

            positionsHistory = positionsHistory.union(newPositions)
        return None

    def hasEnemyInRange(self, unit):
        targets = self.targets(unit)
        return not unit.position.manhattanNeighbours().isdisjoint(map(lambda t: t.position, targets))

    def enemiesInRange(self, unit):
        targets = self.targets(unit)
        es = filter(
            lambda t: t.position in unit.position.manhattanNeighbours(), targets)
        return list(es)

    def round(self):
        self.attacks_this_round = []
        self.moves_this_round = []
        # for each unit
        # identify targets (enemy units) self.targets(unit)
        # identify open squares (open adjacent squares to enemy units)
        #   if not in range already
        #       move towards range of enemy, if reachable
        #       single step (in reading order)
        #   attack if in range
        # self.units.sort(key=lambda unit: unit.position)
        # units_by_reading_order = sorted(
        #    self.units.values(), key=lambda unit: unit.position)
        unit_index = 0
        while unit_index < len(self.units):
            unit = self.units[unit_index]
            # for unit in self.units:

            if not self.hasEnemyInRange(unit):
                targets = self.targets(unit)
                if len(targets) == 0:
                    return False
                open_squares = set().union(*map(lambda target: self.open_squares(target), targets))

                closest_open_square = self.closest(unit, open_squares)
                # Unit is not standing on a closest square, but there exist an open_square
                if unit.position is not closest_open_square and closest_open_square is not None:
                    other_units = self.units.copy()
                    other_units.remove(unit)
                    temp_board = self.board.copy()
                    for u in other_units:
                        temp_board[u.position] = WALL

                    direction = unit.position.shortest_path_direction(
                        closest_open_square, temp_board)
                    unit.move(direction)
                    self.moves_this_round.append(unit)
                    self.units
                # print(self.pretty_str())

            # Has moved or has not moved, w/e time to see if we can attack

            if self.hasEnemyInRange(unit):
                # the adjacent target with the fewest hit points is selected;
                # in a tie, the adjacent target with the fewest
                # hit points which is first in reading order is selected.
                enemies = self.enemiesInRange(unit)
                enemies.sort(key=lambda unit: (unit.hit_points, unit.position))
                victim = enemies[0]
                victim.hit_points -= unit.attack_power
                if victim.hit_points <= 0:
                    victim_index = self.units.index(victim)
                    self.units.remove(victim)
                    if victim_index < unit_index:
                        unit_index -= 1

                # For pretty_str
                self.attacks_this_round.append(unit)
            unit_index += 1

        self.units.sort(key=lambda u: u.position)
        self.round_count += 1
        return True

    def pretty_healthstats(self):
        self.units.sort(key=lambda u: u.position)
        buckets: Dict[int, List[Unit]] = dict()
        for unit in self.units:
            if unit.position.y not in buckets:
                buckets[unit.position.y] = []
            buckets[unit.position.y].append(unit)

        pretty_list = []
        for bucket_key in sorted(buckets.keys()):
            b = buckets[bucket_key]
            for node in b:
                pretty_list.append(f"{node.allegiance}({node.hit_points})\t")
            pretty_list.append("\n")
        return "".join(pretty_list)

    def pretty_str(self):
        max_x = max(map(lambda coord: coord.x, self.board.keys()))
        max_y = max(map(lambda coord: coord.y, self.board.keys()))
        coord_to_unit = dict()
        for unit in self.units:
            coord_to_unit[unit.position] = unit
        pretty_list = []
        for y in range(max_y+1):
            for x in range(max_x+1):

                current_coord = Coord(x, y)
                if current_coord in coord_to_unit:
                    u = coord_to_unit[current_coord]
                    #print("Hello", u, self.attacks_this_round)
                    unit_str = coord_to_unit[current_coord].allegiance.value
                    if u in self.moves_this_round:
                        unit_str = bold(unit_str)
                    if u in self.attacks_this_round:
                        unit_str = red(unit_str)
                    pretty_list.append(unit_str)
                elif current_coord in self.board:
                    pretty_list.append(
                        self.board[current_coord].__repr__())
                else:
                    pretty_list.append('.')
            pretty_list.append('\n')
        return "".join(pretty_list)

    def number_of_living_elves(self):
        return len(list(filter(lambda u: u.allegiance is Allegiace.ELF, self.units)))


def part1(filename):
    #f = open("day_15.movement.example.data")
    f = open(filename)
    game = parse(f)
    f.close()
    print(game.pretty_str())
    # number of full rounds that were completed
    # the sum of the hit points of all remaining units
    completed = True

    while completed:
        completed = game.round()
        # print(game.pretty_healthstats())
        print(game.pretty_str())
    # print(game.pretty_str())

    #print("Rounds", rounds)
    #print("Sum of hit_points", hit_point_sum)
    #print("Res: ", res)
    return game


def part2(filename):
    f = open(filename)
    game = parse(f)
    f.close()
    print(game.pretty_str())
    # the sum of the hit points of all remaining units

    lowest_attack_power = 3
    highest_attack_power = 25
    game.setElvesAttackPower(highest_attack_power)
    number_of_elves_at_start = game.number_of_living_elves()

    completed = True
    while completed:
        completed = game.round()
        # print(game.pretty_healthstats())
        print(game.pretty_str())
    # print(game.pretty_str())
    number_of_elves_at_end = game.number_of_living_elves()
    success = number_of_elves_at_start is number_of_elves_at_end
    print("Did all elves survive?", success)
    #print("Rounds", rounds)
    #print("Sum of hit_points", hit_point_sum)
    #print("Res: ", res)
    return game


if __name__ == "__main__":
    game = part1("day_15.data")
    rounds = game.round_count
    hit_point_sum = sum(map(lambda u: u.hit_points, game.units))
    res = rounds * hit_point_sum
    print("Part1 res:", rounds, hit_point_sum, rounds * hit_point_sum)

    game = part2("day_15.data")
    rounds = game.round_count
    hit_point_sum = sum(map(lambda u: u.hit_points, game.units))
    res = rounds * hit_point_sum
    print("Part2 res:", rounds, hit_point_sum, rounds * hit_point_sum)
