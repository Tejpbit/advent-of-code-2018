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
    
    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

north = Coord(0, -1)
south = Coord(0, 1)
west = Coord(-1, 0)
east = Coord(1, 0)