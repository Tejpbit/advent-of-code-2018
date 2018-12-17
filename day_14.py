from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import math


@dataclass
class Elf:
    currentRecipeIndex: int
    currentStartMarker: str
    currentEndMarker: str

    def findNextRecipe(self, board: List[int]):
        steps_forward = board[self.currentRecipeIndex] + 1
        self.currentRecipeIndex = (
            self.currentRecipeIndex + steps_forward) % len(board)

    def currentRecipe(self, board: List[int]):
        return board[self.currentRecipeIndex]


def part1(input):

    board = [3, 7]
    elves = [
        Elf(0, '(', ')'),
        Elf(1, '[', ']')
    ]
    recipe_count = 2
    while True:
        recipeSum = sum(map(lambda elf: elf.currentRecipe(board), elves))
        for char in list(str(recipeSum)):
            digit = int(char)
            board.append(digit)
            recipe_count += 1
            if recipe_count >= input + 10:
                return "".join(map(str, board[-10:]))
        for elf in elves:
            elf.findNextRecipe(board)


def part2(input):
    listified_input = list(map(int, input))
    sequenceLength = len(listified_input)
    board = [3, 7]
    elves = [
        Elf(0, '(', ')'),
        Elf(1, '[', ']')
    ]
    recipe_count = 2
    while True:
        recipeSum = sum(map(lambda elf: elf.currentRecipe(board), elves))
        for char in list(str(recipeSum)):
            digit = int(char)
            board.append(digit)
            recipe_count += 1
            if board[-sequenceLength:] == listified_input:
                return recipe_count - sequenceLength
        for elf in elves:
            elf.findNextRecipe(board)


if __name__ == "__main__":

    # print(part1(147061))
    print(part2("147061"))
