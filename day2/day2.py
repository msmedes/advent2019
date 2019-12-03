'''https://adventofcode.com/2019/day/2'''

from typing import List


def read_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        return [int(code) for code in f.readline().split(',')]


def process_instruction(arr: List[int], index: int):
    one, two, three, four = arr[index], arr[index +
                                            1], arr[index+2], arr[index+3]
    if one == 1:
        arr[four] = arr[two] + arr[three]
    if one == 2:
        arr[four] = arr[two] * arr[three]


def iterate_instructions(intcodes: List[int]):
    for i in range(0, len(intcodes), 4):
        if intcodes[i] != 99:
            process_instruction(intcodes, i)
        else:
            break


def main():
    target = 19690720
    noun, verb = 0, 99
    intcodes = [0]
    while intcodes[0] != target:
        intcodes = read_file("input.txt")
        intcodes[1], intcodes[2] = noun, verb
        iterate_instructions(intcodes)
        if intcodes[0] < target:
            noun += 1
        if intcodes[0] > target:
            verb -= 1
    print(100 * noun + verb)


if __name__ == '__main__':
    main()
