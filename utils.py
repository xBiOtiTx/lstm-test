from enum import Enum
import numpy as np


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def move(self, offset):
        self.x += offset.x
        self.y += offset.y

    def move(self, tuple):
        self.x += tuple[0]
        self.y += tuple[1]


class Direction(Enum):

    def __init__(self, x, y):
        self.offset = np.array((x, y))

    def x(self):
        return self.offset[0]

    def y(self):
        return self.offset[1]

    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)
