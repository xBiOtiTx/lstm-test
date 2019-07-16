import pygame
import random


class Game1:
    def __init__(self, size):
        from utils import Point
        self.size = size
        self.all_positions = [Point(i, j) for i in range(size) for j in range(size)]
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

    # TODO
    # def restart(self):
    #     pass

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


class Renderer:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (125, 125, 125)
    LIGHT_BLUE = (64, 128, 255)
    GREEN = (0, 200, 64)
    GREEN_DARK = (0, 255, 0)
    YELLOW = (225, 225, 0)
    PINK = (230, 50, 230)

    def __init__(self, surface, game_size):
        self.surface = surface

        self.width = surface.get_width()
        self.height = surface.get_height()

        self.columns = game_size[0]
        self.lines = game_size[1]

        self.cell_width = self.width / self.columns
        self.cell_height = self.height / self.lines

    def set_cell(self, color, column, line):
        pygame.draw.rect(self.surface, color, (column * self.cell_width,
                                               (self.lines - line) * self.cell_height - self.cell_height,
                                               self.cell_width, self.cell_height))

    def render(self, game):
        self.surface.fill((0, 0, 0))

        self.set_cell(Renderer.GREEN, game.position.x, game.position.y)
        self.set_cell(Renderer.YELLOW, game.food.x, game.food.y)

        # for column in range(game.size):
        #     for line in range(game.size):
        #         if game_map[column][line] != 0:
        #             self.set_cell(Renderer.GREEN, column, line)

        pygame.display.update()
