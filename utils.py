from enum import Enum
import numpy as np


class Point:

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 0:
            self.x = 0
            self.y = 0
        elif args_len == 1 and isinstance(args[0], Point):
            self.x = args[0].x
            self.y = args[0].y
        elif args_len == 1 and isinstance(args[0], tuple):
            self.x = args[0][0]
            self.y = args[0][1]
        elif args_len == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            self.x = args[0]
            self.y = args[1]
        else:
            raise ValueError(
                "takes 0 or 1 positional argument with type of <{}> "
                "or 1 positional argument with type of <tuple> "
                "or 2 positional arguments with type of <{}> but <{}> "
                "were given".format("Point", "int", args))

    def __str__(self):
        return [self.x, self.y].__str__()

    def __repr__(self):
        return self.__str__()

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.x * self.y

    def move(self, offset):
        self.x += offset.x
        self.y += offset.y
        return self

    def set(self, other):
        self.x = other.x
        self.y = other.y

    def copy(self):
        return Point(self.x, self.y)


class Direction(Enum):
    def __init__(self, dx, dy):
        self.offset = Point(dx, dy)

    LEFT = -1, 0
    UP = 0, 1
    RIGHT = 1, 0
    DOWN = 0, -1
