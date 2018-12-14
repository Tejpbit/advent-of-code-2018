from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import re
import math
import asyncio

serial_number = 1133
#f = open('11.data')
#f = open('11.example.data')

# The power level in a given fuel cell can be found through the following process:

# Find the fuel cell's rack ID, which is its X coordinate plus 10.
# Begin with a power level of the rack ID times the Y coordinate.
# Increase the power level by the value of the grid serial number (your puzzle input).
# Set the power level to itself multiplied by the rack ID.
# Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
# Subtract 5 from the power level.


@dataclass(eq=True, frozen=True)
class Coord:
    x: int
    y: int

    def moveByCoord(self, step):
        return Coord(self.x+step.x, self.y+step.y)

    def move(self, xStep, yStep):
        return Coord(self.x+xStep, self.y+yStep)

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


def powerLevel(x, y, serial_number=serial_number):
    rack_id = x+10
    power_level = rack_id*y
    power_level += serial_number
    power_level *= rack_id
    power_level = int(power_level / 100) % 10
    power_level -= 5
    return power_level


def generate_cell_grid(serial_number):
    fuelCells: Dict[Coord, int] = dict()
    for x in range(1, 301):
        for y in range(1, 301):
            fuelCells[Coord(x, y)] = powerLevel(
                x, y, serial_number=serial_number)
    return fuelCells


def sum3x3(c: Coord, fuelCells):
    s = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            s += fuelCells[c.move(x, y)]
    return s


def get_max_coord(fuelCells):

    max3x3Coord: Coord = Coord(-1, -1)
    max3x3PowerLevel: int = -math.inf

    for x in range(2, 300):
        for y in range(2, 300):
            c = Coord(x, y)
            s = sum3x3(c, fuelCells)
            if s > max3x3PowerLevel:
                print(s)
                max3x3Coord = c
                max3x3PowerLevel = s
    return(max3x3Coord, max3x3PowerLevel)


#assert(powerLevel(122, 79, 57) == -5)
#assert(powerLevel(217, 196, 39) == 0)
#assert(powerLevel(101, 153, 71) == 4)

def sumXxX(c: Coord, width, fuelCells):
    s = 0
    for x in range(width):
        for y in range(width):
            s += fuelCells[c.move(x, y)]
    return s


async def apa(x, y, width, fuelCells):
    c = Coord(x, y)
    return (c, width, sumXxX(c, width, fuelCells))


async def get_max_coord_part_2(fuelCells):

    tasks = []

    for width in range(1, 301):
        print("newwidth", width)
        for x in range(1, 301-width):
            for y in range(1, 301-width):
                tasks.append(
                    asyncio.create_task(apa(x, y, width, fuelCells))
                )

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close
    ress = await asyncio.gather(*tasks)
    maxXxXCoord: Coord = Coord(-1, -1)
    maxXxXWidth: int = 0
    maxXxXPowerLevel: int = -math.inf
    for res in ress:
        # await t
        (coord, width, powerLevel) = res
        if powerLevel > maxXxXPowerLevel:
            print(maxXxXPowerLevel)
            maxXxXCoord = coord
            maxXxXWidth = width
            maxXxXPowerLevel = powerLevel
    return(maxXxXCoord, maxXxXWidth, maxXxXPowerLevel)


async def main():

    cell_grid = generate_cell_grid(18)
    (maxXxXCoord, maxXxXPowerLevel) = await get_max_coord_part_2(cell_grid)
    print(maxXxXCoord, maxXxXPowerLevel)

@dataclass
class Square:
    top_left: Coord
    bottom_right: Coord

    current_sum: int

    def expand(self, cell_grid):
        if(self.bottom_right.x == 300 or self.bottom_right.y == 300):
            return False
        if(self.bottom_right.x - self.top_left.x > 60):
            return False
        self.bottom_right = self.bottom_right.move(1,1)
        #print(self.bottom_right)
        top_right = Coord(self.bottom_right.x, self.top_left.y)
        bottom_left = Coord(self.top_left.x, self.bottom_right.y)

        new_coord_on_right_side = top_right
        new_coord_on_bottom_side = bottom_left

        new_coords = [self.bottom_right]
        while (new_coord_on_right_side != new_coord_on_bottom_side):
            new_coords.append(new_coord_on_right_side)
            new_coords.append(new_coord_on_bottom_side)
            new_coord_on_bottom_side = new_coord_on_bottom_side.move(1,0)
            new_coord_on_right_side = new_coord_on_right_side.move(0,1)

        for c in new_coords:
            self.current_sum += cell_grid[c]
        return True
        



def part2(serial_number):
    cell_grid = generate_cell_grid(serial_number)

    squares = []
    for x in range(1, 301):
        for y in range(1, 301):
            c = Coord(x,y)
            squares.append(Square(c, c, cell_grid[c]))

    max_power = 0
    max_coord = None
    max_size = 0
    for square in squares:
        #print("nextsquare", square)
        if max_power < square.current_sum:
                max_power = square.current_sum
                max_coord = square.top_left
                max_size = square.bottom_right.x - square.top_left.x
        while(square.expand(cell_grid)):
            if max_power < square.current_sum:
                max_power = square.current_sum
                max_coord = square.top_left
                max_size = square.bottom_right.x - square.top_left.x
                print(max_power, max_coord, max_size)
    print(max_power, max_coord, max_size)



    # cell_start = Coord(90,269)
    # square = Square(cell_start, cell_start, cell_grid[cell_start])
    # print(square.current_sum)
    # while(square.expand(cell_grid)):
    #     print(square.current_sum)



part2(1133)
#asyncio.run(main())

# Part1
#cellGrid = generate_cell_grid(1133)
#(max3x3Coord, max3x3PowerLevel) = get_max_coord(cellGrid)
#print(max3x3Coord.move(-1, -1), max3x3PowerLevel)
