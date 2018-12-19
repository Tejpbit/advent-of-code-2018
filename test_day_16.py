#!/usr/local/bin/python3
import unittest
from typing import List, Tuple, Dict, Set
from util import Coord
import day_16

class Test_Day16(unittest.TestCase):
    
    def test_example1(self):
        s = day_16.Sample("Before: [3, 2, 1, 1]", "9 2 1 2", "After:  [3, 2, 2, 1]")
        opcodes = day_16.possibleOpcodesForSample(s)
        self.assertSetEqual(set(opcodes), {"addi", "seti", "mulr"})

    def test_gtir(self):
        machine = [1,2,3,4]
        day_16.gtir(machine, 3, 1, 2)
        self.assertEqual(machine, [1,2,1,4])

        machine = [1,2,3,4]
        day_16.gtir(machine, 2, 1, 2)
        self.assertEqual(machine, [1,2,0,4])



if __name__ == '__main__':
    unittest.main()