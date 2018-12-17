from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set  # , OrderedDict
import functools
import collections
import math

from util import Coord

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

    def __init__(self, board, units):
        self.board = board
        self.units = sorted(units, key=lambda unit: unit.position)

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

    def round(self):
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
        for unit in self.units:
            targets = self.targets(unit)
            open_squares = set().union(*map(lambda target: self.open_squares(target), targets))

            closest_open_square = self.closest(unit, open_squares)
            if unit.position is closest_open_square or closest_open_square == None:
                pass
                # skip to attack
            else:
                other_units = self.units.copy()
                other_units.remove(unit)
                temp_board = self.board.copy()
                for u in other_units:
                    temp_board[u.position] = WALL

                direction = unit.position.shortest_path_direction(
                    closest_open_square, temp_board)
                unit.move(direction)
                self.units
            print(self.pretty_str())
        self.units.sort(key=lambda u: u.position)

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
                    pretty_list.append(
                        coord_to_unit[current_coord].allegiance.value)
                elif current_coord in self.board:
                    pretty_list.append(self.board[current_coord].__repr__())
                else:
                    pretty_list.append('.')
            pretty_list.append('\n')
        return "".join(pretty_list)


def part1():
    f = open("day_15.movement.example.data")
    game = parse(f)
    print(game.pretty_str())
    while True:
        game.round()
    pass


if __name__ == "__main__":
    part1()
