from tkinter import *
from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import re
import math

f = open('10.data')
#f = open('10.example.data')


@dataclass()
class Coord:
    x: int
    y: int
    velX: int
    velY: int

    def move(self):
        self.x = self.x+self.velX
        self.y = self.y+self.velY

    def moveSteps(self, steps: int):
        self.x = self.x+self.velX*steps
        self.y = self.y+self.velY*steps

    def manhattanDistTo(self, coord: 'Coord'):
        return abs(self.x - coord.x) + abs(self.y - coord.y)


lines = f.readlines()

a = []
reg = re.compile('(-?\d+)')

maxX = -math.inf
maxY = -math.inf
minX = math.inf
minY = math.inf


for line in lines:
    match = reg.findall(line)
    c = Coord(int(match[0]), int(match[1]), int(match[2]), int(match[3]))
    if int(match[0]) > maxX:
        maxX = int(match[0])
    if int(match[1]) > maxY:
        maxY = int(match[1])
    if int(match[0]) < minX:
        minX = int(match[0])
    if int(match[1]) < minY:
        minY = int(match[1])
    a.append(c)

print(minX, minY, " ", maxX, maxY)


def prettyPrint(a: List[Coord]):
    matrix = [['.' for x in range(minX, maxX+1)] for y in range(minY, maxY+1)]
    for c in a:
        matrix[c.y][c.x] = 'x'

    print("\n".join(list(map(lambda x: "".join(x), matrix))))


def round(a: List[Coord], stepSize):

    for a in a:
        a.moveSteps(stepSize)


master = Tk()

canvas_width = 20000
canvas_height = 10000

w = Canvas(master, width=canvas_width, height=canvas_height)
w.pack()

w.create_rectangle(50, 20, 150, 80, fill="black")
w.create_rectangle(0, 0, canvas_width, canvas_height, fill="white")


def printMinMaxBox(coords: List[Coord]):
    maxX = -math.inf
    maxY = -math.inf
    minX = math.inf
    minY = math.inf

    for c in coords:
        if c.x > maxX:
            maxX = c.x
        if c.y > maxY:
            maxY = c.y
        if c.x < minX:
            minX = c.x
        if c.y < minY:
            minY = c.y
    print(minX, minY, " ", maxX, maxY)


def nextFrame(coords: List[Coord], stepSize: int, totalSteps: int):
    print("hello")
    round(a, stepSize)
    w.create_rectangle(0, 0, canvas_width, canvas_height, fill="white")
    for c in coords:
        w.create_rectangle(c.x, c.y, c.x+1, c.y+1, fill="black")
    w.update()

    print(totalSteps)
    printMinMaxBox(coords)

    i = input("A")
    print(i)
    if i == "":
        master.after(1, lambda: nextFrame(a, stepSize, totalSteps+stepSize))
    elif i == 'n':
        newStepSize = int(input("newstepsize"))
        master.after(1, lambda: nextFrame(a, newStepSize, totalSteps+stepSize))


master.after(1, lambda: nextFrame(a, 100, 0))

mainloop()
