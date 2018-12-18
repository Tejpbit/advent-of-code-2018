import copy
from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import collections
import math

regA = 0
regB = 1
regC = 2
regD = 3


def addr(machine, A, B, C):
    machine[regC] = machine[regA] + machine[regB]


def addi(machine, A, B, C):
    machine[regC] = machine[regA] + B


def mulr(machine, A, B, C):
    machine[regC] = machine[regA] * machine[regB]


def muli(machine, A, B, C):
    machine[regC] = machine[regA] * B


def banr(machine, A, B, C):
    machine[regC] = machine[regA] & machine[regB]


def bani(machine, A, B, C):
    machine[regC] = machine[regA] & B


def borr(machine, A, B, C):
    machine[regC] = machine[regA] ^ machine[regB]


def bori(machine, A, B, C):
    machine[regC] = machine[regA] ^ B


def setr(machine, A, B, C):
    machine[regC] = machine[regA]


def seti(machine, A, B, C):
    machine[regC] = A


def gtir(machine, A, B, C):
    machine[regC] = 1 if A > machine[regB] else 0


def gtri(machine, A, B, C):
    machine[regC] = 1 if machine[regA] > B else 0


def gtrr(machine, A, B, C):
    machine[regC] = 1 if machine[regA] > machine[regB] else 0


def eqir(machine, A, B, C):
    machine[regC] = 1 if A == machine[regB] else 0


def eqri(machine, A, B, C):
    machine[regC] = 1 if machine[regA] == B else 0


def eqrr(machine, A, B, C):
    machine[regC] = 1 if machine[regA] == machine[regB] else 0


operations = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr
}


@dataclass
class Sample:
    before: str
    instruction: str
    after: str

    def beforeTm(self):
        parts = self.before.split(" ")
        return [int(parts[1][1:-1]), int(parts[2][:-1]), int(parts[3][:-1]), int(parts[4][:-1])]

    def afterTm(self):
        parts = self.after.split(" ")
        return [int(parts[2][1:-1]), int(parts[3][:-1]), int(parts[4][:-1]), int(parts[5][:-1])]

    def instructionParts(self):
        parts = self.instruction.split(" ")
        return (parts[0], int(parts[1]), int(parts[2]), int(parts[3]))


def parseSamples(lineGen):
    samples = []
    while True:
        before = next(lineGen).strip()
        instruction = next(lineGen).strip()
        if before is "" and instruction is "":
            return samples
        after = next(lineGen).strip()

        _ = next(lineGen)

        samples.append(Sample(before, instruction, after))


def part1(filename):
    f = open(filename)
    lines = f.readlines()
    lineGen = (l for l in lines)
    samples = parseSamples(lineGen)

    matches_3_opcodes = 0
    for sample in samples:
        beforeTm = sample.beforeTm()
        afterTm = sample.afterTm()
        (opcode, A, B, C) = sample.instructionParts()
        count = 0
        for opcode in operations.keys():
            beforeTmCopy = beforeTm.copy()
            operations[opcode](beforeTmCopy, A, B, C)
            if beforeTmCopy == afterTm:
                count += 1
                print(f"{opcode} matches")
        print(count)
        if count > 3:
            matches_3_opcodes += 1
    print(f"matches_3_opcodes: {matches_3_opcodes}, samples {len(samples)}")


if __name__ == "__main__":
    print(part1("day_16.data"))
