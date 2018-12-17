from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import re
import math
import asyncio


@dataclass(eq=True, frozen=True)
class Coord:
    x: int
    y: int

    def moveByCoord(self, step):
        return Coord(self.x+step.x, self.y+step.y)

    def move(self, xStep, yStep):
        return Coord(self.x+xStep, self.y+yStep)

    def turnClockwise(self):
        x = -self.y
        y = self.x
        return Coord(x, y)

    def turnCounterClockwise(self):
        return self.turnClockwise().turnClockwise().turnClockwise()

    def neighbours(self):
        return {
            self.move(0, 1),
            self.move(1, 0),
            self.move(0, -1),
            self.move(-1, 0),
            self.move(1, 1),
            self.move(-1, 1),
            self.move(-1, -1),
            self.move(1, -1)
        }

    def manhattanNeighbours(self):
        return {
            self.move(0, 1),
            self.move(1, 0),
            self.move(0, -1),
            self.move(-1, 0),
        }

    def manhattanDistance(self, to: "Coord"):
        return abs(self.x-to.x) + abs(self.y-to.y)

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def shortest_path_direction(self, other: "Coord", blocks: Set["Coord"]):
        distance_grid = dict()
        new_coords = set()
        new_coords.add(other)

        distance = 0
        while len(new_coords) is not 0:
            for coord in new_coords:
                distance_grid[coord] = distance

            if self in distance_grid:
                direction_to_distance = []
                for ordinal in [north, south, west, east]:
                    c = self.moveByCoord(ordinal)
                    if c in distance_grid:
                        direction_to_distance.append(
                            (ordinal, distance_grid[c], c))
                # direction_to_distance = list(map(lambda ordinal: (ordinal, distance_grid[self.moveByCoord(ordinal)]), [
                #    north, south, west, east]))
                direction_to_distance.sort(
                    key=lambda tuple: (tuple[1], tuple[2]))
                # key=lambda tuple: tuple[1])
                return direction_to_distance[0][0]

                # New coord are the union of all one-manhattan step neighbours to previous cords
                # but remove the ones which are blocked
                # and remove the ones we've already visited
            new_coords = set().union(
                *map(lambda coord: coord.manhattanNeighbours(), new_coords)
            ).difference(blocks).difference(set(distance_grid.keys()))
            distance += 1


north = Coord(0, -1)
south = Coord(0, 1)
west = Coord(-1, 0)
east = Coord(1, 0)
