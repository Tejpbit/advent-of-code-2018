from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools

#f = open("06.example.data")
f = open("06.data")
lines = f.readlines()


a = map(lambda x: x.strip().split(', '), lines)
a = map(lambda x: tuple(x), a)
a = map(lambda x: (int(x[0]), int(x[1])), a)
a = list(a)



@dataclass(eq=True, frozen=True)
class Coord:
    x: int
    y: int

    def move(self, step):
        return Coord(self.x+step.x, self.y+step.y)

    def neighbours(self):
        return {
            self.move(Coord(0, 1)),
            self.move(Coord(1, 0)),
            self.move(Coord(0, -1)),
            self.move(Coord(-1, 0))
        }
    
    def manhattanDistTo(self, coord: 'Coord'):
        return abs(self.x - coord.x) + abs(self.y - coord.y)


@dataclass
class Spreader:
    name: str
    origin: Coord
    area: Set[Coord]
    newArea: Set[Coord]
    lastNewArea: Set[Coord]

    def spreaderNeighbours(self):
        n = map(lambda x: x.neighbours(), self.newArea)
        n = set.union(set(), *n)
        n = list(filter(lambda c: c not in self.area, n))
        return n
    
    def clearNewArea(self):
        #self.lastNewArea = self.newArea
        self.newArea = set()

    def size(self):
        return len(self.area)


Grid = Dict[Coord, Spreader]

def addToGrid(grid: Grid, at: Coord, spreader: Spreader):
    if at in grid:
        grid[at] = None
    else:
        grid[at] = spreader

def merge(dest: Grid, src: Grid, spreaders: List[Spreader]):
    for k in src:
        if src[k]:
            src[k].area.add(k)
            src[k].newArea.add(k)
        dest[k] = src[k]
    


def prettyPrint(grid: Grid):
    xMax =  max(
        map(lambda c: c.x, grid.keys())
    )
    yMax =  max(
        map(lambda c: c.y, grid.keys())
    )
    strBuilder = ""
    for y in range(yMax):
        for x in range(xMax):
            if Coord(x,y) not in grid:
                strBuilder += " "
                continue
            cell = grid[Coord(x,y)]
            if cell:
                strBuilder += cell.name
            else:
                strBuilder += "."
        strBuilder += '\n'

    return strBuilder


def round(grid, spreaders):
    #gridAdditions: Grid = {}
    additionsThisRound: Dict[Coord, Spreader] = dict()
    for spreader in spreaders.values():
        neightbours = spreader.spreaderNeighbours()
        spreader.clearNewArea()
        for nCoord in neightbours:
            if nCoord not in grid:
                grid[nCoord] = spreader
                spreader.newArea.add(nCoord)
                additionsThisRound[nCoord] = spreader
            elif nCoord in additionsThisRound.keys() and additionsThisRound[nCoord] != None:
                grid[nCoord] = None
                additionsThisRound[nCoord].newArea.remove(nCoord)
                additionsThisRound[nCoord] = None
    for (coord, spreader) in additionsThisRound.items():
        if not spreader == None:
            spreader.area.add(coord)
                    
    
    
def part1():

    names = list(map(chr, range(48, 48+len(a))))
    spreaders: Dict[str, Spreader] = dict()
    for (name, s) in zip(names, a):
        spreaders[name] = Spreader(name, Coord(s[0], s[1]), {Coord(s[0], s[1])}, {Coord(s[0], s[1])}, set())

    grid: Grid = {}

    for spreader in spreaders.values():
        addToGrid(grid, spreader.origin, spreader)

    for i in range(100):
        print(prettyPrint(grid))
        print(i)
        m = map(lambda s: (s.name, s.size()), spreaders.values())
        m = list(m)
        m = sorted(m, key=lambda x: x[1], reverse=True)
        print("Sizes", m[:30])
        
        #input("Continue...")
        round(grid, spreaders)
    

@dataclass
class Point:
    name: str
    coord: Coord


def part2():
    names = list(map(chr, range(48, 48+len(a))))
    points: Dict[Point] = dict()
    for (name, coord) in zip(names, a):
        points[name] = Point(name, Coord(coord[0], coord[1]))
    
    print(points)
    xs = list(map(lambda p: p.coord.x, points.values()))
    xMin =  min(xs)
    xMax =  max(xs)
    ys = list(map(lambda p: p.coord.y, points.values()))
    yMax =  max(ys)
    yMin =  min(ys)
    print(xMin, xMax, yMin, yMax)

    coordsInArea = set()
    for x in range(xMin, xMax+1):
        for y in range(yMin, yMax+1):
            distSum = 0
            for point in points.values():
                distSum += point.coord.manhattanDistTo(Coord(x,y))
            if distSum < 10_000:
                coordsInArea.add(Coord(x,y))
    
    print("Size: ", len(coordsInArea))



part2()