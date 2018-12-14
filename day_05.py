
from concurrent.futures import ThreadPoolExecutor
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
    (last, q) = reduce(asd, polymerstring, ('', ""))
    q = q + last
    prevQ = polymerstring
    while len(prevQ) != len(q):
        print(chr(27) + "[2J")
        print(q)
        prevQ = q
        (last, q) = reduce(asd, q, ('', ""))
        q = q+last
    return q

from time import sleep
def reduceMax2(polymerstring):
    polymerlist = list(polymerstring)
    cursor = 0
    while cursor < len(polymerlist)-1:
        if is_match(polymerlist[cursor],polymerlist[cursor+1]):
            del1 = polymerlist.pop(cursor+1)
            del2 = polymerlist.pop(cursor)
            cursor -= 1 if cursor > 0 else 0
        else:
            cursor += 1
    return polymerlist

reducedPolymer = reduceMax2(polymerstring)
print(len(reducedPolymer))

def parallelReduceMax2(name, polymer, return_dict):
    return_dict[name] = reduceMax2(polymer)

threads = []
results = []

from multiprocessing import Process, Manager
shortest = ("", __import__('math').inf)
for c in "abcdefghijklmnopqrstuvwxyz":
    a = [x for x in reducedPolymer if x != c and x != c.capitalize()]
    
    polymer = reduceMax2(a)
    if(len(polymer) < shortest[1]):
        shortest = (f'Removed {c}', len(polymer))

    

print(shortest[0], shortest[1])