from typing import List


def read_file(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(line.strip()) for line in f.readlines()]


def fuel(mass: int) -> int:
    return (mass//3) - 2


def sum_fuel(masses: List[int]) -> int:
    return sum(fuel(mass) for mass in masses)


def fuel_for_fuel(mass: int) -> int:
    total = 0
    curr_fuel = fuel(mass)
    while curr_fuel >= 0:
        total += curr_fuel
        curr_fuel = fuel(curr_fuel)
    return total


def main():
    masses = read_file("input.txt")
    print(sum_fuel(masses))
    print(sum(fuel_for_fuel(mass) for mass in masses))


if __name__ == "__main__":
    main()
