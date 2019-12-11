from typing import List, NamedTuple, Tuple


from math import pi, atan2, sqrt
from collections import defaultdict


class Asteroid(NamedTuple):
    x: int
    y: int


Asteroids = List[Asteroid]


def read_file(filename="input.txt") -> Asteroids:
    with open(filename) as f:
        return create_asteroids(f.read())


def create_asteroids(raw: str) -> Asteroids:
    return [
        Asteroid(x, y)
        for y, line in enumerate(raw.strip().split('\n'))
        for x, char in enumerate(line)
        if char == "#"
    ]


def get_angle(a: Asteroid, b: Asteroid):
    return atan2(b.x - a.x, a.y - b.y) % (2 * pi)


def calc_visible(center: Asteroid, asteroids: Asteroids):
    angles = set()
    for asteroid in asteroids:
        if asteroid is not center:
            angle = get_angle(center, asteroid)
            angles.add(angle)
    return len(angles)


def most_detected(asteroids: Asteroids) -> Tuple[Asteroid, int]:
    visibilities = [(asteroid, calc_visible(asteroid, asteroids))
                    for asteroid in asteroids]

    return max(visibilities, key=lambda tup: tup[1])


# part 1
asteroids = read_file()
print(most_detected(asteroids))

# part 2


def distance(a: Asteroid, b: Asteroid) -> float:
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y)**2)


def blast_em(center: Asteroid, asteroids: Asteroids) -> Asteroids:
    order = []
    # create a dict of all asteroids on an angle
    angles = defaultdict(list)

    for asteroid in asteroids:
        angles[get_angle(center, asteroid)].append(asteroid)

    # sort by distance so we can remove the closest asteroids first
    for asteroids in angles.values():
        asteroids.sort(key=lambda a: distance(center, a), reverse=True)

    # while we still have angles left
    while angles:
        # arctan2 returns angles in a clockwise fashion so that's taken care of,
        # we just need to sort the keys in the dict
        vals = angles.keys()
        vals = sorted(vals)

        # blast em
        for angle in vals:
            asteroids = angles[angle]
            order.append(asteroids.pop())
            if not asteroids:
                del angles[angle]

    return order


if __name__ == '__main__':
    asteroids = read_file()
    most = most_detected(asteroids)
    twohundy = blast_em(most[0], asteroids)[199]
    print(twohundy.x * 100 + twohundy.y)
