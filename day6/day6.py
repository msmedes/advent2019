from typing import List, Tuple, Dict, Set, DefaultDict
import time
from collections import defaultdict, deque

Orbits = DefaultDict[str, Set[str]]


def read_file(file_name: str) -> List[List[str]]:
    with open(file_name) as f:
        return [line.strip().split(")") for line in f.readlines()]


def add_orbits(orbits: List[str]) -> Orbits:
    orbit_map = defaultdict(set)
    for orbit in orbits:
        orbit_map[orbit[0]].add(orbit[1])
        orbit_map[orbit[1]].add(orbit[0])
    return orbit_map


def count_orbits(orbits: Orbits):
    count = defaultdict(int)

    for obj in orbits.keys():
        curr_obj = orbits[obj]
        while curr_obj != 'COM':
            count[obj] += 1
            curr_obj = orbits[curr_obj]
        count[obj] += 1

    print(sum(count.values()))


def bfs(orbits: Orbits, root: str, target: str) -> int:
    if root not in orbits:
        return f'root node {root} not in orbits.'
    if target not in orbits:
        return f'Target node {target} not in orbits'

    visited, queue = set(), deque([root])
    while queue:
        path = queue.popleft()
        obj = path[-1]
        if obj not in visited:
            for neighbor in orbits[obj]:
                if neighbor != obj:
                    curr_path = list(path)
                    curr_path.append(neighbor)
                    if neighbor == target:
                        return curr_path
                    queue.append(curr_path)
            visited.add(obj)


# test = ['COM)B',
#         'B)C',
#         'C)D',
#         'D)E',
#         'E)F',
#         'B)G',
#         'G)H',
#         'D)I',
#         'E)J',
#         'J)K',
#         'K)L',
#         'K)1',
#         'I)2']

# test = [line.split(')') for line in test]
# test = add_orbits(test)
orbits = read_file("input.txt")
orbits = add_orbits(orbits)
print(len(bfs(orbits, '1', '2')))
