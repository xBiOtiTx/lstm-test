import random

from Point import Point


class Game1:
    def __init__(self, size):
        self.size = size
        self.all_positions = set(Point(i, j) for i in range(size) for j in range(size))
        self.map = [[0 for i in range(size)] for j in range(size)]
        self.position = Point(size // 2, size // 2)
        self.food = self.init_food(self.position)
        self.score = 0
        self.step = 0
        self.gameover = False

    def init_food(self, position):
        food_test = self.all_positions.copy()
        food_test.remove(position)
        return random.choice(food_test)

    def move(self, offset):
        self.step += 1
        if self.test_move(offset):
            self.position.move(offset)
            if self.position == self.food:
                self.score += 1
                self.food = self.init_food(self.position)
        else:
            self.gameover = True
        return not self.gameover

    def test_move(self, offset):
        t = self.position.copy()
        t.move(offset)
        return 0 <= t.x < self.size and 0 <= t.y < self.size
