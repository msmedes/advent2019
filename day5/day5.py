from typing import List, Tuple


def parse_instruction(instruction: str) -> Tuple[int]:
    opcode = instruction % 100

    mode_1 = (instruction // 100) % 10  # hundredths
    mode_2 = (instruction // 1000) % 10  # thousandths
    mode_3 = (instruction // 10000) % 10  # tenthousandths

    return opcode, mode_1, mode_2, mode_3


def read_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        return [int(code) for code in f.readline().split(',')]


def iterate_instructions(program: List[int], input_val: int):
    pos = 0
    output = 0
    val1, val2 = 0, 0
    while program[pos] != 99:
        opcode, mode1, mode2, mode3 = parse_instruction(program[pos])

        if opcode not in [3, 4]:
            val1, val2 = get_values(program, pos, mode1, mode2)

        if opcode == 1:
            program[program[pos + 3]] = val1 + val2
            pos += 4
        elif opcode == 2:
            program[program[pos + 3]] = val1 * val2
            pos += 4
        elif opcode == 3:
            location = program[pos+1]
            program[location] = input_val
            pos += 2
        elif opcode == 4:
            location = program[pos+1]
            output = program[location]
            pos += 2
        elif opcode == 5:
            pos = val2 if val1 != 0 else pos + 3
        elif opcode == 6:
            pos = val2 if val1 == 0 else pos + 3
        elif opcode == 7:
            program[program[pos+3]] = 1 if val1 < val2 else 0
            pos += 4
        elif opcode == 8:
            program[program[pos+3]] = 1 if val1 == val2 else 0
            pos += 4

    return output


def get_values(program: List[int], pos, mode1, mode2) -> Tuple[int]:
    val1 = program[program[pos + 1]] if mode1 == 0 else program[pos+1]
    val2 = program[program[pos + 2]] if mode2 == 0 else program[pos+2]
    return val1, val2


program = read_file("input.txt")
print(iterate_instructions(program, 5))
