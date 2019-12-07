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


# assert not is_valid_part2(112223)

count = 0
for i in range(171309, 643604):
    if is_valid_part2(i):
        count += 1

print(count)
