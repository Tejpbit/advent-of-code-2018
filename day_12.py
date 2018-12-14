from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import re
import math
import asyncio

initial_state = "#.#####.##.###...#...#.####..#..#.#....##.###.##...#####.#..##.#..##..#..#.#.#.#....#.####....#..#"

raw_rules = [
    "#.#.. => .",
    "..### => .",
    "...## => .",
    ".#### => #",
    ".###. => #",
    "#.... => .",
    "#.#.# => .",
    "###.. => #",
    "#..#. => .",
    "##### => #",
    ".##.# => #",
    ".#... => .",
    "##.## => #",
    "#...# => #",
    ".#.## => .",
    "##..# => .",
    "..... => .",
    ".#.#. => #",
    "#.### => #",
    "....# => .",
    "...#. => #",
    "..#.# => #",
    "##... => #",
    "####. => #",
    "#..## => #",
    "##.#. => #",
    "###.# => .",
    "#.##. => .",
    "..#.. => #",
    ".#..# => .",
    "..##. => .",
    ".##.. => #"
]

@dataclass
class Rule:
    pattern: List[chr]
    result: chr

    def matches(self, that: List[chr]):
        return self.pattern == that

@dataclass
class State:
    pots: Dict[int, chr]

    def __init__(self, pots):
        self.pots = dict()
        for i, pot in enumerate(pots):
            if pot == "#":
                self.pots[i] = pot

    def __repr__(self):

        res = []
        #for i in range(min(self.pots.keys()), 1+max(self.pots.keys())):
        #print(min(self.pots.keys()), max(self.pots.keys()))
        for i in range(-40, 500):
            res.append(self.get(i))
        return "".join(res)

    def number_sum(self):
        return sum(self.pots.keys())

    def get(self, index):
        if index not in self.pots:
            return '.'
        return self.pots[index]

    def get_window(self, start, end):
        window = []
        for i in range(start,end+1):
            window.append(self.get(i))
        return window

    def next_generation(self, rules):
        next_gen = State("")

        current = min(self.pots.keys())-2
        end = max(self.pots.keys())+4
        while current <= end:
            w = self.get_window(current-2, current+2)
            for rule in rules:
                if rule.matches(w):
                    if rule.result == "." and current in next_gen.pots:
                        del next_gen.pots[current]
                    if rule.result == "#":
                        next_gen.pots[current] = rule.result
                    break
                
            current += 1
        return next_gen
            


def parse_rule(str):
    parts = str.split(" => ")
    return Rule(list(parts[0]), parts[1])



def main():
    # initial_state = "#..#.#..##......###...###"
    # raw_rules = [
    #     "...## => #",
    #     "..#.. => #",
    #     ".#... => #",
    #     ".#.#. => #",
    #     ".#.## => #",
    #     ".##.. => #",
    #     ".#### => #",
    #     "#.#.# => #",
    #     "#.### => #",
    #     "##.#. => #",
    #     "##.## => #",
    #     "###.. => #",
    #     "###.# => #",
    #     "####. => #"
    # ]
    state = State(initial_state)
    rules = []
    for r in raw_rules:
        rules.append(parse_rule(r))
    print("             1         2         3     ")
    print("   0         0         0         0     ")
    print(state)
    # for i in range(20):
    #     state = state.next_generation(rules)
    #     print(state)

    # print(state.number_sum())

    for i in range(1,1000+1):
        
        state = state.next_generation(rules)
        print(min(state.pots.keys()), max(state.pots.keys()))
        print(state)

    print(state.number_sum())
    #for i in range(20):
        
main()

def main2():
    gen500 = (400, 593)
    gen1000 = (gen500[0]+1000-500, gen500[1]+1000-500)
    gen50billion = (gen500[0]+50000000000-500, gen500[1]+50000000000-500)
    print("1000", sum(n for n in range(gen1000[0], gen1000[1]+1)))
    print("50000000000", sum(n for n in range(gen50billion[0], gen50billion[1]+1)))

    
    print(gen50billion)


main2()