#!/usr/local/bin/python3
from enum import Enum
import copy
from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import collections
import math
import copy
from util import Coord


class Ground:
    water_spring: Coord
    clay_set: Set[Coord]
    water_set: Set[Coord] = set()

    def xRange(self):
        xs = list(map(lambda c: c.x, self.clay_set))
        xMin = min(xs)
        xMax = max(xs)
        return range(xMin, xMax+1)

    def yRange(self):
        ys = list(map(lambda c: c.y, self.clay_set))
        yMin = min(ys)
        yMax = max(ys)
        return range(0, yMax+1)

    def __init__(self, water_spring, clay_set):
        self.water_spring = water_spring
        self.clay_set = clay_set
        first_water_coord = water_spring.move(0, 1)
        self.water_set.add(first_water_coord)

    def tick(self):
        water_list = sorted(self.water_set.values())
        water_list.reverse()
        new_water = set()
        for water in water_list:
            nWater = water.tick(self)
            new_water.update(nWater)

        for w in new_water:
            self.water_set[w.coord] = w

        return None


def parse(file):
    clay_set: Set[Coord] = set()

    lines = file.readlines()
    for line in lines:
        xCoordStart = None
        xCoordEnd = None
        yCoordStart = None
        yCoordEnd = None
        parts = line.strip().split(", ")
        if parts[0].startswith("x"):
            xCoordStart = int(parts[0].split("=")[1])
            xCoordEnd = xCoordStart
            yCoordParts = parts[1].split("=")[1].split("..")
            yCoordStart = int(yCoordParts[0])
            yCoordEnd = int(yCoordParts[1])
        else:  # starts with y
            yCoordStart = int(parts[0].split("=")[1])
            yCoordEnd = yCoordStart
            xCoordParts = parts[1].split("=")[1].split("..")
            xCoordStart = int(xCoordParts[0])
            xCoordEnd = int(xCoordParts[1])

        for x in range(xCoordStart, xCoordEnd+1):
            for y in range(yCoordStart, yCoordEnd+1):
                clay_set.add(Coord(x, y))
    return clay_set


def prettyPrint(ground: Ground):
    clay_set = ground.clay_set
    water_spring = ground.water_spring
    water_coord_set = ground.water_set
    xs = list(map(lambda c: c.x, clay_set))
    xMin = min(xs)
    xMax = max(xs)
    ys = list(map(lambda c: c.y, clay_set))
    yMax = max(ys)
    #yMin = min(ys)

    pretty_list = []
    for y in range(0, yMax+1):
        for x in range(xMin, xMax+1):
            if Coord(x, y) == water_spring:
                pretty_list.append("+")
            elif Coord(x, y) in clay_set:
                pretty_list.append("#")
            elif Coord(x, y) in water_coord_set:
                pretty_list.append("~")
            else:
                pretty_list.append(".")
        pretty_list.append("\n")
    return "".join(pretty_list)


def part1(ground: Ground):
    previous_water_count = -1
    while previous_water_count != len(ground.water_set):
        previous_water_count = len(ground.water_set)
        ground.tick()
        print(prettyPrint(ground))


def part1_try_2(ground: Ground):

    return part1_try_2_rec(ground, ground.water_spring.move(0, 1))


class FloodingFeedback(Enum):
    OUT_OF_BOUNDS = 1
    FULL = 2


def part1_try_2_rec(ground: Ground, coord: Coord) -> bool:
    groundXRange = ground.xRange()
    groundYRange = ground.yRange()
    inbounds = coord.x in groundXRange and coord.y in groundYRange
    if inbounds:
        ground.water_set.add(coord)
    else:
        return FloodingFeedback.OUT_OF_BOUNDS

    # print(prettyPrint(ground))
    below = coord.moveByCoord(Coord(0, 1))
    right = coord.moveByCoord(Coord(1, 0))
    left = coord.moveByCoord(Coord(-1, 0))

    downFeedback = False
    rightFeedback = True
    leftFeedback = True
    emptyBelow = below not in ground.clay_set and below not in ground.water_set
    if emptyBelow:
        downFeedback = part1_try_2_rec(ground, below)
        if downFeedback == FloodingFeedback.OUT_OF_BOUNDS:
            return FloodingFeedback.OUT_OF_BOUNDS
    if right not in ground.clay_set and right not in ground.water_set:
        rightFeedback = part1_try_2_rec(ground, right)
    if left not in ground.clay_set and left not in ground.water_set:
        leftFeedback = part1_try_2_rec(ground, left)
    if (rightFeedback == FloodingFeedback.OUT_OF_BOUNDS or
            leftFeedback == FloodingFeedback.OUT_OF_BOUNDS):
        return FloodingFeedback.OUT_OF_BOUNDS

    return FloodingFeedback.FULL


if __name__ == "__main__":
    #f = open("day_17.example.data")
    f = open("day_17.data")
    clay_set = parse(f)
    water_spring = Coord(x=500, y=0)
    g = Ground(water_spring, clay_set)
    # print(prettyPrint(g))
    part1_try_2(g)
    print(len(g.water_set))
