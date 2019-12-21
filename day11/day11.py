from intcode import Intcode, EndProgram

from typing import List, Tuple

from collections import defaultdict
from enum import Enum


Panel = Tuple[int, int]


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Robot():
    def __init__(self, program: List[int]):
        self.panels = defaultdict(lambda: 0)
        self.painted = set()
        self.computer = Intcode(program)
        self.direction = Direction.UP
        self.message = set()

    def __call__(self,):
        curr_panel = 0, 0
        self.panels[curr_panel] = 1
        try:
            while True:
                curr_color = self.panels[curr_panel]
                color_to_paint = self.computer([curr_color])
                turn = self.computer([])
                self.panels[curr_panel] = color_to_paint
                self.painted.add(curr_panel)
                self._set_direction(turn)
                curr_panel = self._move(turn, curr_panel)

        except EndProgram:
            self.message = {cell for cell,
                            color in self.panels.items() if color == 1}

    def _move(self, turn: int, panel: Panel) -> Panel:
        '''
        if direction is up or down: x axis change
        if direction is left or right, direction is y axis
        '''
        x, y = panel
        if self.direction == Direction.UP:
            panel = x, y + 1
        elif self.direction == Direction.RIGHT:
            panel = x + 1, y
        elif self.direction == Direction.DOWN:
            panel = x, y - 1
        elif self.direction == Direction.LEFT:
            panel = x - 1, y
        return panel

    def _set_direction(self, turn: int):
        if self.direction == Direction.UP:
            self.direction = Direction.LEFT if turn == 0 else Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.UP if turn == 0 else Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.RIGHT if turn == 0 else Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN if turn == 0 else Direction.UP

    def display(self):
        x_min, x_max = min(x for (x, y) in self.message), max(
            x for (x, y) in self.message)
        y_min, y_max = min(y for (x, y) in self.message), max(
            y for (x, y) in self.message)
        output = ''
        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                if (x, y) in self.message:
                    output += '*'
                else:
                    output += ' '
            output += '\n'
        return output


def read_file(file_name="input.txt") -> List[int]:
    with open(file_name) as f:
        return [int(code) for code in f.readline().strip().split(',')]


robot = Robot(read_file())
robot()
print(robot.display())
