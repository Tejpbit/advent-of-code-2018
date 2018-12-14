import re
from dataclasses import dataclass
from typing import List, Set, Dict
import functools

f = open('data/07.data')
#f = open('data/07.example.data')
lines = f.readlines()

p = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin\.')


@dataclass
class Node:
    name: str
    traversed: bool
    parents: Set["Node"]
    children: Set["Node"]
    secondsUntilCompleted: int

    def __init__(self, name, traversed, parents, children):
        self.name = name
        self.traversed = traversed
        self.parents = parents
        self.children = children
        self.secondsUntilCompleted = 60 + ord(name[0]) - 64

    def __hash__(self):
        return hash(self.name)

    def available(self):
        return all(map(lambda x: x.traversed, self.parents))

    def doOneWork(self):
        self.secondsUntilCompleted -= 1

    def completed(self):
        return self.secondsUntilCompleted == 0


# nodes: Dict[str, Node]
tree: Node
nodes: Dict[str, Node] = dict()
for line in lines:
    parts = p.findall(line.strip())[0]
    nodes[parts[0]] = (Node(parts[0], False, set(), set()))
    nodes[parts[1]] = (Node(parts[1], False, set(), set()))

for line in lines:
    [before, after] = p.findall(line.strip())[0]
    nodes[before].children.add(nodes[after])
    nodes[after].parents.add(nodes[before])


def roots(nodes: Dict[str, Node]):
    roots: Set[Node] = set()
    for node in nodes.values():
        if not node.parents:
            roots.add(node)
    return roots


rs = roots(nodes)
# print(list(map(lambda x: x.name, rs)))


def traverseAlphabetically(roots: Set[Node]):
    unlockedNodes = list(roots)
    while unlockedNodes:
        unlockedNodes = sorted(unlockedNodes, key=lambda x: x.name)
        n = unlockedNodes.pop(0)
        n.traversed = True
        for child in n.children:
            if all(map(lambda x: x.traversed, child.parents)):
                unlockedNodes += [child]
        yield n


def part1():
    for node in traverseAlphabetically(rs):
        print(node.name, end="")


def part2(rs: Set[Node]):
    workers = 5
    availableNodes = sorted(list(rs), key=lambda x: x.name)
    activeNodes = set()

    for n in availableNodes:
        print(f"{n.name}, {n.secondsUntilCompleted}")

    while 0 < len(availableNodes) and len(activeNodes) < 5:
        activeNodes.add(availableNodes.pop(0))
    seconds = 0
    while True:
        for n in activeNodes:
            n.doOneWork()
        seconds += 1

        doneNodes = set(filter(lambda x: x.completed(), activeNodes))
        activeNodes = activeNodes.difference(doneNodes)

        for n in doneNodes:
            n.traversed = True
            for child in n.children:
                if child.available():
                    availableNodes += [child]

        availableNodes = list(sorted(availableNodes, key=lambda x: x.name))
        while 0 < len(availableNodes) and len(activeNodes) < workers:
            activeNodes.add(availableNodes.pop(0))

        if len(activeNodes) == 0:
            break

    print("Total working time: ", seconds)


part2(rs)
