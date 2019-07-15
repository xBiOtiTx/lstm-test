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

    def __init__(self, offset):
        self.offset = offset

    UP = Point(0, 1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, -1)
    LEFT = Point(-1, 0)
