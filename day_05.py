

import asyncio
from functools import reduce
f = open("data/05.data")

lines = f.readlines()

polymerstring = lines[0]


from threading import Lock
import _thread

def is_match(c1, c2):
    return (c1.islower() and c1.capitalize() == c2) or (c1.isupper() and c1.lower() == c2)
    #return ord(c1) ^ ord(c2) == 32

def asd(acc, future):
    (prev, newStr) = acc
    if not is_match(prev, future):
        return (future, newStr+prev)
    return ('', newStr)


def reduceMax(polymerstring):
    polymerlist = list(polymerstring)
    cursor = 0
    while cursor < len(polymerlist)-1:
        if is_match(polymerlist[cursor],polymerlist[cursor+1]):
            del polymerlist[cursor+1]
            del polymerlist[cursor]
            cursor -= 1 if cursor > 0 else 0
        else:
            cursor += 1
    return polymerlist

reducedPolymer = reduceMax(polymerstring)
print(len(reducedPolymer))

async def reduceMaxRoutine(name, polymerstr):
    return (name, reduceMax)

routines = []

from multiprocessing import Process, Manager
shortest = ("", __import__('math').inf)
for c in "abcdefghijklmnopqrstuvwxyz":
    a = [x for x in reducedPolymer if x != c and x != c.capitalize()]
    
    routine = reduceMaxRoutine(f'Removed {c}', a)
    routines += [routine]

asyncio.gather(routines...)


    

print(shortest[0], shortest[1])