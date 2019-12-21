from typing import NamedTuple, List, Dict, Union

from collections import defaultdict, deque
from pprint import pprint
import math


raw = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''

raw2 = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''


def make_ingredient(ingredient: str):
    parts = ingredient.split(" ")
    return {"ingredient": parts[1], "amount": int(parts[0])}


def create_recipes(line: str, recipes):
    inputs, output = line.split(" => ")

    ingredients = [make_ingredient(ingredient)
                   for ingredient in inputs.split(', ')]

    output = make_ingredient(output)

    recipes[output["ingredient"]] = {
        "servings": output["amount"], "ingredients": ingredients}

    return recipes


def create_fuel(amount, recipes):
    ORE = "ORE"

    leftover = defaultdict(int)
    queue = deque([{"ingredient": "FUEL", "amount": amount}])
    ore = 0
    while queue:
        curr = queue.popleft()
        if curr["ingredient"] == ORE:
            ore += curr["amount"]
        elif curr["amount"] <= leftover[curr["ingredient"]]:
            leftover[curr["ingredient"]] -= curr["amount"]
        else:
            needed = curr["amount"] - leftover[curr["ingredient"]]
            recipe = recipes[curr["ingredient"]]
            servings = math.ceil(needed/recipe["servings"])
            [queue.append({"ingredient": ingredient["ingredient"], "amount": ingredient["amount"] * servings})
             for ingredient in recipe["ingredients"]]
            remainder = servings * recipe["servings"] - needed
            leftover[curr["ingredient"]] = remainder

    return ore


def all_the_ore(recipes) -> int:
    high = 1e10
    low = 1
    capacity = 1e12
    mid = 0

    while low + 1 < high:
        mid = low + ((high - low) // 2)

        ore = create_fuel(mid, recipes)

        if ore <= capacity:
            low = mid
        else:
            high = mid
    return mid


def parse_input(filename="input.txt"):
    recipes = {}
    with open(filename) as f:
        # for line in raw.split("\n"):
        for line in f.readlines():
            create_recipes(line.strip(), recipes)

    return recipes


recipes = parse_input()
# pprint(recipes)

print(all_the_ore(recipes))
