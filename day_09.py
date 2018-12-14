
from dataclasses import dataclass
from typing import List, Set, Dict
import functools


@dataclass
class Node:
    next: "Node"
    previous: "Node"
    marbleValue: int

    def __init__(self, marbleValue):
        self.next = self
        self.previous = self
        self.marbleValue = marbleValue

    def add(self, n: "Node"):
        self.next.previous = n
        n.next = self.next
        n.previous = self
        self.next = n
        return n

    def remove(self):
        newCurrent = self.next
        self.previous.next = self.next
        self.next.previous = self.previous
        return (self, newCurrent)

    def backSeven(self):
        return self.previous.previous.previous.previous.previous.previous.previous

    def __repr__(self):
        return __str__(self)

    def __str__(self):
        nodeZero = self
        while nodeZero.marbleValue != 0:
            nodeZero = nodeZero.next

        lastValue = nodeZero.previous.marbleValue
        current = nodeZero
        values = []
        while current.marbleValue != lastValue:
            values.append(current.marbleValue)
            current = current.next
        values.append(current.marbleValue)
        return " ".join([str(x) for x in values])


def addScore(scoreBoard, player, value):
    if not player in scoreBoard:
        scoreBoard[player] = 0
    scoreBoard[player] += value


def players(numberOfPlayers):
    while(True):
        for n in range(1, numberOfPlayers+1):
            yield n


def part1(numberOfPlayers, maxMarble):
    playerGen = players(numberOfPlayers)

    marbles = (n for n in range(1, maxMarble+1))
    currentPlayer = next(playerGen)
    score = dict()
    circle = Node(0)

    for m in marbles:
        if m % 23 == 0:
            addScore(score, currentPlayer, m)
            circle = circle.backSeven()
            (removed, newCurrent) = circle.remove()
            circle = newCurrent
            addScore(score, currentPlayer, removed.marbleValue)
        else:
            circle = circle.next.add(Node(m))
        currentPlayer = next(playerGen)
        # print(circle)
    return max(score.values())


print(part1(9, 25))
print(part1(10, 1618))
print(part1(13, 7999))

print("part1: ", part1(493, 71863))
print("part2: ", part1(493, 71863*100))
