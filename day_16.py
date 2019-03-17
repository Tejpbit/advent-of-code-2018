#!/usr/local/bin/python3
import copy
from dataclasses import dataclass
from typing import NewType, List, Tuple, Dict, Set
import functools
import collections
import math
import copy

regA = 0
regB = 1
regC = 2
regD = 3


def addr(machine, A, B, C):
    machine[C] = machine[A] + machine[B]


def addi(machine, A, B, C):
    machine[C] = machine[A] + B


def mulr(machine, A, B, C):
    machine[C] = machine[A] * machine[B]


def muli(machine, A, B, C):
    machine[C] = machine[A] * B


def banr(machine, A, B, C):
    machine[C] = machine[A] & machine[B]


def bani(machine, A, B, C):
    machine[C] = machine[A] & B


def borr(machine, A, B, C):
    machine[C] = machine[A] ^ machine[B]


def bori(machine, A, B, C):
    machine[C] = machine[A] ^ B


def setr(machine, A, B, C):
    machine[C] = machine[A]


def seti(machine, A, B, C):
    machine[C] = A


def gtir(machine, A, B, C):
    machine[C] = 1 if A > machine[B] else 0


def gtri(machine, A, B, C):
    machine[C] = 1 if machine[A] > B else 0


def gtrr(machine, A, B, C):
    machine[C] = 1 if machine[A] > machine[B] else 0


def eqir(machine, A, B, C):
    machine[C] = 1 if A == machine[B] else 0


def eqri(machine, A, B, C):
    machine[C] = 1 if machine[A] == B else 0


def eqrr(machine, A, B, C):
    machine[C] = 1 if machine[A] == machine[B] else 0


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


def possibleOpcodesForSample(sample: Sample):
    beforeTm = sample.beforeTm()
    afterTm = sample.afterTm()
    (opcode, A, B, C) = sample.instructionParts()
    possibleOpCodes = []
    for opcode in operations.keys():

        beforeTmCopy = beforeTm.copy()
        operations[opcode](beforeTmCopy, A, B, C)

        if beforeTmCopy == afterTm:
            possibleOpCodes.append(opcode)
    return possibleOpCodes


def part1(filename):
    f = open(filename)
    lines = f.readlines()
    lineGen = (l for l in lines)
    samples = parseSamples(lineGen)

    matches_3_opcodes = 0
    for sample in samples:
        beforeTm = sample.beforeTm()
        afterTm = sample.afterTm()
        (_, A, B, C) = sample.instructionParts()
        count = 0
        for opcode in operations.keys():
            beforeTmCopy = beforeTm.copy()
            operations[opcode](beforeTmCopy, A, B, C)
            if beforeTmCopy == afterTm:
                count += 1
        if count >= 3:
            matches_3_opcodes += 1
    return f"matches_3_opcodes: {matches_3_opcodes}, samples {len(samples)}"


def execute_program(number_to_opcode, lineGen):
    machine = [0, 0, 0, 0]
    for line in lineGen:
        parts = list(map(int, line.split(" ")))
        opcode = number_to_opcode[parts[0]]
        operations[opcode](machine, *parts[1:])
        print("hello")


@dataclass()
class Statement:
    op_number: int
    op_codes: Set[str]

    def merge(self, other: "Statement"):
        if self.op_number != other.op_number:
            raise Exception("Can only merge same op_numbers")
        return Statement(self.op_number, self.op_codes.intersection(other.op_codes))

    def reduce_by_assumption(self, assumptions: Dict[int, str]):
        for a in assumptions:
            if a == self.op_number:
                self.op_codes = self.op_codes.intersection({assumptions[a]})
            else:
                self.op_codes = self.op_codes.difference({assumptions[a]})

    def __copy__(self):
        return Statement(self.op_number, self.op_codes.copy())

    def __deepcopy__(self, memo):
        return Statement(self.op_number, self.op_codes.copy())

    # def reduce_by_statements(self, statements: Dict[int, Statement]):

    def pretty_str(self):
        return f"{self.op_number}: {self.op_codes}"

    def isDetermined(self):
        return len(self.op_codes) == 1


def part2_solver(statements: Dict[str, Statement], assumptions: Dict[int, str] = dict()):
    ress = []
    statements = copy.deepcopy(statements)
    # Apply assumptions
    for key in statements:
        statements[key].reduce_by_assumption(assumptions)
        #statements[a] = assumption[a]

    if(any(map(lambda op_num: len(statements[op_num].op_codes) == 0, statements))):
        #print("nope", list(map(lambda s: s.pretty_str(), statements.values())))
        return None
    if all(map(lambda op_num: len(statements[op_num].op_codes) == 1, statements)):
        return statements
    else:  # not solved, walk through all possible assumptions from all undetermined statements
        undeterminedStatements = (
            s for s in statements.values() if not s.isDetermined())

        for unresolvedStatement in undeterminedStatements:
            for op_code in unresolvedStatement.op_codes:
                s = copy.deepcopy(statements)
                s[unresolvedStatement.op_number] = Statement(
                    unresolvedStatement.op_number, {op_code})
                a = copy.deepcopy(assumptions)
                a[unresolvedStatement.op_number] = op_code
                res = part2_solver(s, a)
                if res:
                    ress.append(res)
    if len(ress) > 0:
        return ress
    else:
        return None


def part2(filename):
    f = open(filename)
    lines = f.readlines()
    lineGen = (l for l in lines)
    samples = parseSamples(lineGen)

    statement_merger: Dict[int, Statement] = dict()
    for sample in samples:
        beforeTm = sample.beforeTm()
        afterTm = sample.afterTm()
        (int_op_code, A, B, C) = sample.instructionParts()

        statement = Statement(int_op_code, set())
        for opcode in operations:
            beforeTmCopy = beforeTm.copy()
            operations[opcode](beforeTmCopy, A, B, C)

            if beforeTmCopy == afterTm:
                statement.op_codes.add(opcode)

        if statement.op_number not in statement_merger:
            statement_merger[statement.op_number] = statement
        else:
            statement_merger[statement.op_number] = statement_merger[statement.op_number].merge(
                statement)

    s = part2_solver(statement_merger)

    print("part2:", s)

    #execute_program(determined_number_to_opcode, lineGen)

    return None


if __name__ == "__main__":
    print(part1("day_16.data"))
    print(part2("day_16.data"))
