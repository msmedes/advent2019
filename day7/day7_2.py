from typing import List, Tuple, Iterator

from enum import Enum
from collections import deque
import itertools


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    END = 99


class Amplifier():
    def __init__(self, program: List[int], phase: int):
        self.input_queue = deque([phase])
        self.phase = phase
        self.program = program[:]
        self.pos = 0

    def run_program(self, input_val: int):
        self.input_queue.append(input_val)
        val1, val2 = 0, 0
        while True:
            opcode, mode1, mode2, mode3 = parse_instruction(
                self.program[self.pos])

            if opcode == Opcode.END:
                return None

            if opcode not in [Opcode.INPUT, Opcode.OUTPUT]:
                val1, val2 = get_values(self.program, self.pos, mode1, mode2)

            if opcode == Opcode.ADD:
                self.program[self.program[self.pos + 3]] = val1 + val2
                self.pos += 4
            elif opcode == Opcode.MULTIPLY:
                self.program[self.program[self.pos + 3]] = val1 * val2
                self.pos += 4
            elif opcode == Opcode.INPUT:
                location = self.program[self.pos+1]
                self.program[location] = self.input_queue.popleft()
                self.pos += 2
            elif opcode == Opcode.OUTPUT:
                location = self.program[self.pos+1]
                output = self.program[location]
                self.pos += 2
                return output
            elif opcode == Opcode.JUMP_TRUE:
                self.pos = val2 if val1 != 0 else self.pos + 3
            elif opcode == Opcode.JUMP_FALSE:
                self.pos = val2 if val1 == 0 else self.pos + 3
            elif opcode == Opcode.LESS_THAN:
                self.program[self.program[self.pos+3]
                             ] = 1 if val1 < val2 else 0
                self.pos += 4
            elif opcode == Opcode.EQUALS:
                self.program[self.program[self.pos+3]
                             ] = 1 if val1 == val2 else 0
                self.pos += 4


def parse_instruction(instruction: str) -> Tuple[int]:
    opcode = instruction % 100

    mode_1 = (instruction // 100) % 10  # hundredths
    mode_2 = (instruction // 1000) % 10  # thousandths
    mode_3 = (instruction // 10000) % 10  # tenthousandths

    return Opcode(opcode), mode_1, mode_2, mode_3


def read_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        return [int(code) for code in f.readline().split(',')]


def get_values(program: List[int], pos, mode1, mode2) -> Tuple[int]:
    val1 = program[program[pos + 1]] if mode1 == 0 else program[pos+1]
    val2 = program[program[pos + 2]] if mode2 == 0 else program[pos+2]
    return val1, val2


def feedback(program: List[int], phases: List[int]) -> int:
    amps = [Amplifier(program, phase) for phase in phases]
    num_complete, idx, output, thrust_output = 0, 0, 0, 0
    num_amps = len(amps)

    while num_complete < num_amps:
        output = amps[idx].run_program(output)
        if output is None:
            num_complete += 1
        else:
            thrust_output = output
        idx = (idx + 1) % num_amps

    return thrust_output


# def max_signal(program) -> int:
#     max_signal = 0
#     for phase_seq in itertools.permutations([0, 1, 2, 3, 4]):
#         input_signal = 0
#         curr_program = program[:]
#         for amplifier_setting in phase_seq:
#             input_signal, curr_program = run_program(
#                 curr_program, (amplifier_setting, input_signal))
#         max_signal = max(max_signal, input_signal)

#     return max_signal


TEST1 = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27,
         26,  27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]

assert feedback(TEST1, [9, 8, 7, 6, 5]) == 139629729


TEST2 = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1,
         53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]

assert feedback(TEST2, [9, 7, 8, 5, 6]) == 18216


def calc_max(program=read_file("input.txt")) -> int:
    return max(feedback(program, phase)
               for phase in itertools.permutations([5, 6, 7, 8, 9]))


print(calc_max())
