from typing import NewType, List, Tuple, Dict, Set
import functools
f = open("06.data")
lines = f.readlines()


a = map(lambda x: x.strip().split(', '), lines)
a = map(lambda x: tuple(x), a)
a = map(lambda x: (int(x[0]), int(x[1])), a)
a = list(a)


Coord = NewType('Coord', Tuple)


def getX(coord: Coord) -> int:
    return coord[0]


def getY(coord: Coord) -> int:
    return coord[1]


def move(coord: Coord, step: Coord):
    return (coord[0]+step[0], coord[1]+step[1])

def neighbours(coord: Coord):
    return [
        move(coord, (0, 1)),
        move(coord, (1, 1)),
        move(coord, (1, 0)),
        move(coord, (1, -1)),
        move(coord, (0, -1)),
        move(coord, (-1, -1)),
        move(coord, (-1, 0)),
        move(coord, (-1, 1))
    ]

from dataclasses import dataclass

@dataclass
class Spreader:
    name: str
    origin: Coord
    area: Set[Coord]
    newArea: Set[Coord]
    lastNewArea: Set[Coord]

    def spreaderNeighbours(self):
        n = map(neighbours, self.newArea)
        n = [item for sublist in n for item in sublist]
        n = set(n)
        n = list(filter(lambda c: c not in self.area, n))
        return n
    
    def clearNewArea(self):
        #self.lastNewArea = self.newArea
        self.newArea = set()

    def size(self):
        return len(self.area)


#Spreader = Tuple[str, Coord, List[Coord]]

# Maps a grid coord to the origin coords of spreaders who've reched that grid coord
Grid = Dict[Coord, List[Coord]]

names = list(map(chr, range(48, 48+len(a))))
spreaders: List[Spreader] = list(map(lambda x: Spreader(x[0], x[1], set(), {x[1]}, set()), zip(names, a)))
print("spreader!", spreaders)

def name(spreader: Spreader):
    return spreader[0]

grid: Grid = {}

def addToCell(grid: Grid, at: Coord, spreader: Spreader):
    if at not in grid:
        grid[at] = []
    grid[at].append(spreader.name)
    spreader.area.add(at)
    spreader.newArea.add(at)

def occupied(grid: Grid, at: Coord):
    return at in grid

def merge(dest: Grid, src: Grid):
    for k in src:
        dest[k] = src[k]

def prettyPrint(grid: Grid, spreaders: List[Spreader]):
    xMax =  max(
        map(lambda c: getX(c), grid.keys())
    )
    yMax =  max(
        map(lambda c: getY(c), grid.keys())
    )
    strBuilder = ""
    for y in range(yMax):
        for x in range(xMax):
            if (x,y) not in grid:
                strBuilder += " "
                continue
            cell = grid[(x,y)]
            if len(cell) > 1:
                strBuilder += "."
            elif len(cell) == 1:
                strBuilder += cell[0]
        strBuilder += '\n'

    return strBuilder

for spreader in spreaders:
    addToCell(grid, spreader.origin, spreader)


def round(grid, spreaders):
    gridAdditions: Grid = {}
    for spreader in spreaders:
        for n in spreader.spreaderNeighbours():
            if not occupied(grid, n):
                addToCell(gridAdditions, n, spreader)
        
    merge(grid, gridAdditions)


asd = spreaders

print()
print(grid)
for i in range(100):
    print(prettyPrint(grid, spreaders))
    print(i)
    m = map(lambda x: (x.name, x.size()), spreaders)
    m = list(m)
    m = sorted(m, key=lambda x: x[1], reverse=True)
    print("Sizes", m[:30])
    
    #input("Continue...")
    round(grid, spreaders)
    