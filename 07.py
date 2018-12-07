import re
from dataclasses import dataclass
from typing import List, Set, Dict
import functools

f = open('07.data')
#f = open('07.example.data')
lines = f.readlines()

p = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin\.')

@dataclass
class Node:
    name: str
    traversed: bool
    parents: Set["Node"]
    children: Set["Node"]



    def __hash__(self):
        return hash(self.name)


#nodes: Dict[str, Node]
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
print(list(map(lambda x: x.name, rs)))

def traverseAlphabetically(roots: Set[Node]):
    unlockedNodes = list(roots)
    while unlockedNodes:
        unlockedNodes = sorted(unlockedNodes, key=lambda x: x.name)
        n = unlockedNodes.pop(0)
        n.traversed = True
        for child in n.children:
            if all( map(lambda x: x.traversed, child.parents) ):
                unlockedNodes += [child]
        yield n

for node in traverseAlphabetically(rs):
    print(node.name, end="")

