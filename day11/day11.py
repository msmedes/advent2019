from intcode import Intcode, EndProgram

from typing import List, Tuple, Set, Any

from collections import defaultdict
from enum import Enum


Panel = Tuple[int, int]


class Color(Enum):
    BLACK = 0
    WHITE = 1


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
            self.message = {cell for cell, color in self.panels.items() if color == 1}
            print(self.message)

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
        x_min, x_max = min(x for (x, y) in self.message), max(x for (x, y) in self.message)
        y_min, y_max = min(y for (x, y) in self.message), max(y for (x, y) in self.message)
        output = ''
        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                if (x, y) in self.message:
                    output += '*'
                else:
                    output += ' '
            print(output)
            output = ''
            


PROGRAM = [3,8,1005,8,301,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,29,1,1103,7,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,54,2,103,3,10,2,1008,6,10,1006,0,38,2,1108,7,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,91,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,114,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,136,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,158,1,1009,0,10,2,1002,18,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,187,2,1108,6,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,213,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,236,1,104,10,10,1,1002,20,10,2,1008,9,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,269,1,102,15,10,1006,0,55,2,1107,15,10,101,1,9,9,1007,9,979,10,1005,10,15,99,109,623,104,0,104,1,21102,1,932700598932,1,21102,318,1,0,1105,1,422,21102,1,937150489384,1,21102,329,1,0,1105,1,422,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,46325083227,0,1,21102,376,1,0,1106,0,422,21102,3263269927,1,1,21101,387,0,0,1105,1,422,3,10,104,0,104,0,3,10,104,0,104,0,21102,988225102184,1,1,21101,410,0,0,1105,1,422,21101,868410356500,0,1,21102,1,421,0,1106,0,422,99,109,2,21202,-1,1,1,21102,1,40,2,21102,1,453,3,21102,1,443,0,1105,1,486,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,448,449,464,4,0,1001,448,1,448,108,4,448,10,1006,10,480,1102,1,0,448,109,-2,2106,0,0,0,109,4,1201,-1,0,485,1207,-3,0,10,1006,10,503,21101,0,0,-3,22101,0,-3,1,21201,-2,0,2,21102,1,1,3,21101,0,522,0,1105,1,527,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,550,2207,-4,-2,10,1006,10,550,22102,1,-4,-4,1105,1,618,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,569,1,0,1106,0,527,22101,0,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,588,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,610,21201,-1,0,1,21101,610,0,0,105,1,485,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

def read_file(file_name="input.txt") -> List[int]:
    with open(file_name) as f:
        return [int(code) for code in f.readline().strip().split(',')]


robot = Robot(PROGRAM)
robot()
robot.display()
