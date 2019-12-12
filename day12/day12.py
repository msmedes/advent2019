from typing import List
import re

from dataclasses import dataclass
import copy
import math


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def calc_energy(self) -> int:
        return sum([abs(self.x), abs(self.y), abs(self.z)])


class Moon:
    def __init__(self, position: Vector, velocity: Vector = None) -> None:
        self.position = position
        self.velocity = velocity or Vector(0, 0, 0)

    def calc_pe(self) -> int:
        return self.position.calc_energy()

    def calc_ke(self) -> int:
        return self.velocity.calc_energy()

    def total_energy(self) -> int:
        return self.calc_pe() * self.calc_ke()

    def apply_velocity(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    def xs(self):
        return (self.position.x, self.velocity.x)

    def ys(self):
        return (self.position.y, self.velocity.y)

    def zs(self):
        return (self.position.z, self.velocity.z)

    def __repr__(self) -> str:
        return f'Moon(position={self.position}, velocity={self.velocity})\n'


def x_state(moons: List):
    return tuple(moon.xs() for moon in moons)


def y_state(moons: List):
    return tuple(moon.ys() for moon in moons)


def z_state(moons: List):
    return tuple(moon.zs() for moon in moons)


def parse(raw: str):
    moons = []
    lines = raw.strip().split('\n')
    for line in lines:
        coords = re.findall(r'-?\d+', line)
        x, y, z = coords
        moons.append(Moon(Vector(int(x), int(y), int(z))))
    return moons


def compare(vel: int, a: int, b: int):
    if a < b:
        vel += 1
    elif b < a:
        vel -= 1
    return vel


def step(moons: List[Moon]):
    for moon in moons:
        for other in moons:
            if moon != other:
                moon.velocity.x = compare(
                    moon.velocity.x, moon.position.x, other.position.x)
                moon.velocity.y = compare(
                    moon.velocity.y, moon.position.y, other.position.y)
                moon.velocity.z = compare(
                    moon.velocity.z, moon.position.z, other.position.z)

    for moon in moons:
        moon.apply_velocity()


def iterate(moons: List[Moon], state_fn):
    copies = copy.deepcopy(moons)

    seen = set()
    seen.add(state_fn(moons))

    steps = 0

    while True:
        steps += 1
        step(copies)
        state = state_fn(copies)
        if state in seen:
            return steps
        else:
            seen.add(state)


def total_energy(moons: List[Moon]) -> int:
    return sum(moon.total_energy() for moon in moons)


def lcm(a, b):
    return a * b // math.gcd(a, b)


inputs = '''
<x=-16, y=-1, z=-12>
<x=0, y=-4, z=-17>
<x=-11, y=11, z=0>
<x=2, y=2, z=-6>
'''

moons = parse(inputs)
x = iterate(moons, x_state)
y = iterate(moons, y_state)
z = iterate(moons, z_state)


print(lcm(z, lcm(x, y)))
