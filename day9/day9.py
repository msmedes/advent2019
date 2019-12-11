from typing import List, Tuple

from enum import Enum
from collections import deque, defaultdict


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    BASE = 9
    END = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class EndProgram(Exception):
    pass


class Intcode():
    def __init__(self, program: List[int]):
        self.input_queue = deque()
        self.program = defaultdict(
            int, {i: value for i, value in enumerate(program)})
        self.pos = 0
        self.base = 0

    def __call__(self, inputs: List[int]):
        self.input_queue.extend(inputs)
        while True:
            val1, val2, = 0, 0
            opcode, mode1, mode2, mode3 = self._parse_instruction(
                self.program[self.pos])
            if opcode == Opcode.END:
                raise EndProgram

            if opcode not in [Opcode.INPUT, Opcode.OUTPUT]:
                val1 = self._get_value(self.pos + 1, mode1)
                val2 = self._get_value(self.pos + 2, mode2)

            if opcode == Opcode.ADD:
                location = self._location(self.pos + 3, mode3)
                self.program[location] = val1 + val2
                self.pos += 4

            elif opcode == Opcode.MULTIPLY:
                location = self._location(self.pos + 3, mode3)
                self.program[location] = val1 * val2
                self.pos += 4

            elif opcode == Opcode.INPUT:
                location = self._location(self.pos + 1, mode1)
                self.program[location] = self.input_queue.popleft()
                self.pos += 2

            elif opcode == Opcode.OUTPUT:
                value = self._get_value(self.pos + 1, mode1)
                self.pos += 2
                return value

            elif opcode == Opcode.JUMP_TRUE:
                self.pos = val2 if val1 != 0 else self.pos + 3

            elif opcode == Opcode.JUMP_FALSE:
                self.pos = val2 if val1 == 0 else self.pos + 3

            elif opcode == Opcode.LESS_THAN:
                location = self._location(self.pos + 3, mode3)
                self.program[location] = 1 if val1 < val2 else 0
                self.pos += 4

            elif opcode == Opcode.EQUALS:
                location = self._location(self.pos + 3, mode3)
                self.program[location] = 1 if val1 == val2 else 0
                self.pos += 4

            elif opcode == Opcode.BASE:
                value = self._get_value(self.pos + 1, mode1)
                self.base += value
                self.pos += 2

            else:
                raise ValueError(f"invalid opcode: {opcode}")

    def _get_value(self, pos: int, mode: Mode) -> int:
        val = 0
        if mode == Mode.POSITION:
            val = self.program[self.program[pos]]
        elif mode == Mode.IMMEDIATE:
            val = self.program[pos]
        elif mode == Mode.RELATIVE:
            val = self.program[self.program[pos] + self.base]
        return val

    def _parse_instruction(self, instruction: int) -> Tuple[Opcode, Mode, Mode, Mode]:
        opcode = instruction % 100

        mode_1 = (instruction // 100) % 10  # hundredths
        mode_2 = (instruction // 1000) % 10  # thousandths
        mode_3 = (instruction // 10000) % 10  # tenthousandths

        return Opcode(opcode), Mode(mode_1), Mode(mode_2), Mode(mode_3)

    def _location(self, pos: int, mode: Mode) -> int:
        value = 0
        if mode == Mode.POSITION:
            value = self.program[pos]
        if mode == Mode.RELATIVE:
            value = self.base + self.program[pos]
        return value


def read_file(file_name="input.txt") -> List[int]:
    with open(file_name) as f:
        return [int(code) for code in f.readline().strip().split(',')]


def run_program(program: List[int], inputs: List[int]):
    output = []
    computer = Intcode(program)

    try:
        while True:
            output.append(computer(inputs))
            inputs = []

    except EndProgram:
        return output


BOOST = read_file()
print(run_program(BOOST, [2]))
