'''
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 171309-643603.

--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?

Your puzzle input is still 171309-643603
'''

from typing import List
from collections import Counter

Digits = List[int]


def increases(digits: Digits):
    for i in range(len(digits) - 1):
        if digits[i] > digits[i+1]:
            return False
    return True


def doubles(digits: Digits):
    for i in range(len(digits)-1):
        if digits[i] == digits[i+1]:
            return True
    return False


def get_digits(number: int) -> Digits:
    digits = []
    for _ in range(6):
        digit = number % 10
        digits.append(digit)
        number = number//10

    return digits[::-1]


def is_valid(number: str) -> bool:
    digits = get_digits(number)
    return increases(digits) and doubles(digits)


def is_valid_part2(number: str) -> bool:
    digits = get_digits(number)
    return increases(digits) and correct_twos(digits)


def correct_twos(digits: Digits) -> bool:
    counts = Counter(digits)
    return any(count == 2 for count in counts.values())


assert not is_valid_part2(112223)

# count = 0
# for i in range(171309, 643604):
#     if is_valid_part2(i):
#         count += 1

# print(count)
