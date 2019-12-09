from typing import List, Tuple, Iterator

from enum import Enum
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


def parse_instruction(instruction: str) -> Tuple[int]:
    opcode = instruction % 100

    mode_1 = (instruction // 100) % 10  # hundredths
    mode_2 = (instruction // 1000) % 10  # thousandths
    mode_3 = (instruction // 10000) % 10  # tenthousandths

    return Opcode(opcode), mode_1, mode_2, mode_3


def read_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        return [int(code) for code in f.readline().split(',')]


def run_program(program: List[int], input_val: Tuple[int]):
    pos = 0
    output = 0
    val1, val2 = 0, 0
    input_index = 0
    while program[pos] != 99:
        opcode, mode1, mode2, mode3 = parse_instruction(program[pos])

        if opcode not in [Opcode.INPUT, Opcode.OUTPUT]:
            val1, val2 = get_values(program, pos, mode1, mode2)

        if opcode == Opcode.ADD:
            program[program[pos + 3]] = val1 + val2
            pos += 4
        elif opcode == Opcode.MULTIPLY:
            program[program[pos + 3]] = val1 * val2
            pos += 4
        elif opcode == Opcode.INPUT:
            location = program[pos+1]
            program[location] = input_val[input_index]
            input_index += 1
            pos += 2
        elif opcode == Opcode.OUTPUT:
            location = program[pos+1]
            output = program[location]
            pos += 2
        elif opcode == Opcode.JUMP_TRUE:
            pos = val2 if val1 != 0 else pos + 3
        elif opcode == Opcode.JUMP_FALSE:
            pos = val2 if val1 == 0 else pos + 3
        elif opcode == Opcode.LESS_THAN:
            program[program[pos+3]] = 1 if val1 < val2 else 0
            pos += 4
        elif opcode == Opcode.EQUALS:
            program[program[pos+3]] = 1 if val1 == val2 else 0
            pos += 4

    return output, program


def get_values(program: List[int], pos, mode1, mode2) -> Tuple[int]:
    val1 = program[program[pos + 1]] if mode1 == 0 else program[pos+1]
    val2 = program[program[pos + 2]] if mode2 == 0 else program[pos+2]
    return val1, val2


def max_signal(program) -> int:
    max_signal = 0
    for phase_seq in itertools.permutations([0, 1, 2, 3, 4]):
        input_signal = 0
        curr_program = program[:]
        for amplifier_setting in phase_seq:
            input_signal, curr_program = run_program(
                curr_program, (amplifier_setting, input_signal))
        max_signal = max(max_signal, input_signal)

    return max_signal


# assert max_signal([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210
# assert max_signal([3,23,3,24,1002,24,10,24,1002,23,-1,23,
#     101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321

# assert max_signal([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
#     1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210

program = read_file("input.txt")
print(max_signal(program))
