from dataclasses import dataclass
from typing import List, Set, Dict
import functools

#f = open("08.example.data")
f = open("08.data")

line = f.readlines()[0]
data = line.split(" ")
data = map(lambda x: int(x), data)
data = list(data)
nameGenerator = (n for n in range(1, len(data)))
inputGenerator = (n for n in data)


@dataclass
class Node:
    name: str
    parent: "Node"
    children: List["Node"]
    metadata: List[int]


def parse(inputGenerator, nameGenerator, parent: Node):

    childNodesCount = next(inputGenerator)
    metadataCount = next(inputGenerator)

    currentNode = Node(next(nameGenerator), parent, None, None)

    children = []
    for i in range(childNodesCount):
        children.append(parse(inputGenerator, nameGenerator, currentNode))

    metadata = []
    for i in range(metadataCount):
        metadata.append(next(inputGenerator))

    currentNode.children = children
    currentNode.metadata = metadata

    return currentNode


root = parse(inputGenerator, nameGenerator, None)


def metadatasum(tree: Node):
    if len(tree.children) == 0:
        return sum(tree.metadata)
    childrenSums = map(lambda x: metadatasum(x), tree.children)

    return sum(tree.metadata) + sum(childrenSums)


print("part1", metadatasum(root))


def valueOfNode(node: Node):
    if len(node.children) == 0:
        return sum(node.metadata)
    nodeValue = 0
    for i in node.metadata:
        i -= 1
        if i < len(node.children):
            nodeValue += valueOfNode(node.children[i])
    return nodeValue


print("par2", valueOfNode(root))
