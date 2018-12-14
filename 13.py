from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import re
import math
import asyncio

from util import Coord, north, south, west, east

#f = open("13.example.data")
f = open("13.data")
#f = open("13.example-part2.data")

lines = f.readlines()


print(set("".join(lines)))


@dataclass
class Track:
    sign: str
    coord: Coord
    directions: List[Coord]

    def __hash__(self):
        return self.coord.__hash__()

    def next(self, direction: Coord):
        if direction in self.directions:
            return (self.coord.moveByCoord(direction), direction)
        else: # not in direction. we have to turn
            clockWiseDirection = direction.turnClockwise()
            counterClockWiseDireciton = direction.turnCounterClockwise()
            if clockWiseDirection in self.directions:
                return (self.coord.moveByCoord(clockWiseDirection), clockWiseDirection)
            elif counterClockWiseDireciton in self.directions:
                return (self.coord.moveByCoord(counterClockWiseDireciton), counterClockWiseDireciton)
        raise Exception("No direction available")


def prettyPrint(tracks, carts):
    carts_dict = dict()
    for cart in carts:
        carts_dict[cart.position] = cart
    track_coords = list(map(lambda x: x.coord, tracks.values()))
    max_x = max(map(lambda coord: coord.x, track_coords))
    max_y = max(map(lambda coord: coord.y, track_coords ))

    out = []
    for y in range(max_y+1):
        out.append([])
        for x in range(max_x+1):
            c = Coord(x,y)
            if c in carts_dict:
                out[-1].append( carts_dict[c].sign() )
            elif c in tracks:
                out[-1].append( tracks[c].sign )
            else:
                out[-1].append(" ")
    o = ["".join(row) for row in out]
    #print(chr(27) + "[2J")
    print("\n\n\n\n\n\n")
    print("\n".join(o))




crossing_turn_rotation = [
    lambda x: x.turnCounterClockwise(),
    lambda x: x,
    lambda x: x.turnClockwise()
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
@dataclass
class Cart:
    id: str
    position: Coord
    direction: Coord
    next_crossing_turn: int = 0

    def __lt__(self, other):
        return self.position.__lt__(other.position)

    def move(self, tracks):
        current_track = tracks[self.position]
        if current_track.sign == '+':
            turn_function = crossing_turn_rotation[self.next_crossing_turn]
            self.direction = turn_function(self.direction)
            self.next_crossing_turn = (self.next_crossing_turn+1) % 3

        (new_pos, new_direction) = current_track.next(self.direction)
        self.position = new_pos
        self.direction = new_direction

    def sign(self):
        direction_to_str_map = {north: "^", south: "v", west: "<", east: ">"}
        return bcolors.BOLD + bcolors.OKGREEN + direction_to_str_map[self.direction] + bcolors.ENDC

    def str(self):
        return bcolors.BOLD + bcolors.OKGREEN + self.id + bcolors.ENDC


def getDirectionsFromSign(sign):
    if sign == '+':    
        return [north, south, west, east]
    elif sign in ['-', '<', '>']:
        return [west, east]
    elif sign in ['|', 'v', '^']:
        return [north, south]
    return []



def neighbourInDirectionIsVerticalTrack(track, direction, trackParts):
    north_or_south_going_signs = ['|', 'v', '^', '+']
    neighbour_coord = track.coord.moveByCoord(direction)
    if neighbour_coord not in trackParts:
        return False
    if trackParts[neighbour_coord].sign in north_or_south_going_signs:
        return True
    return False


nameGenerator = (chr(n) for n in range(65,126))
def initTrackAndCarts():
    tracks = dict()
    carts = []

    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == " " or cell == "\n":
                continue
            if cell in ['v', '^', '<', '>']:
                a = {'v': south, '^': north, '<': west, '>': east}
                c = Cart(next(nameGenerator), Coord(x,y), a[cell])
                print(c)
                carts.append(c)
            location = Coord(x,y)
            directions = getDirectionsFromSign(cell)
            cellSign = cell
            if cell in ['v', '^']:
                cellSign = "|"
            elif cell in ['<', '>']:
                cellSign = "-"
            t = Track(cellSign, location, directions)
            tracks[location] = t

    for track in tracks.values():

        if track.sign == '/':
            if neighbourInDirectionIsVerticalTrack(track, north, tracks):
                track.directions = [north, west]
            elif neighbourInDirectionIsVerticalTrack(track, south, tracks):
                track.directions = [south, east]
        elif track.sign == '\\':
            if neighbourInDirectionIsVerticalTrack(track, north, tracks):
                track.directions = [north, east]
            elif neighbourInDirectionIsVerticalTrack(track, south, tracks):
                track.directions = [south, west]
    return (tracks, carts)


def firstCollision():
    (tracks, carts) = initTrackAndCarts()
    while True:
        carts.sort(key=lambda x: x.position)
        positions_moved_to_this_turn = set()
        for cart in carts:
            cart.move(tracks)
            if cart.position in positions_moved_to_this_turn:
                print(cart.position)
                return
            positions_moved_to_this_turn.add(cart.position)

#firstCollision()

def lastCartPositionAfterFirstLonesomeTic():
    (tracks, carts) = initTrackAndCarts()
    prettyPrint(tracks, carts)
    count = 0
    while True:
        # if count > 10000:
        #     print(count)
        #     prettyPrint(tracks, carts)
        #     input("Enter to print next")
        #input("Enter to print next")
        #prettyPrint(tracks, carts)
        if len(carts) == 1:
            c = carts[0]
            print("count", count)
            return c
        carts.sort(key=lambda x: x.position)
        positions_moved_to_this_turn = dict()
        coordsToRemoveCartsFrom = set()
        for cart in carts:
            cart.move(tracks)
            if cart.position in positions_moved_to_this_turn:
                #input("Enter to print next")
                print("\n\n\n\n")
                print(f"tick: {count}, Crash at ({cart.position.x},{cart.position.y}) {cart.str()}, {positions_moved_to_this_turn[cart.position].str()}")
                #prettyPrint(tracks, carts)
                print("carts after crash", sorted(carts,key=lambda x: x.position))
                coordsToRemoveCartsFrom.add(cart.position)
                del positions_moved_to_this_turn[cart.position]
            else:
                positions_moved_to_this_turn[cart.position] = cart
        carts = list(filter(lambda x: x.position not in coordsToRemoveCartsFrom, carts))
        count += 1
c = lastCartPositionAfterFirstLonesomeTic()
print(f"Final cart: {c.str()}, {c.position}")
#print(carts)

             
        
        