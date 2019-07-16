import random


def main_game(q):
    import pygame
    from render import Renderer
    from pygame.constants import QUIT
    from utils import Direction
    import numpy as np

    TICK_RATE = 100
    WIDTH = 800
    HEIGHT = 800
    SIZE = 3

    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game1(SIZE)
    renderer = Renderer(surface, (SIZE, SIZE))
    game_counter = 0

    timer = pygame.time.get_ticks()
    while True:
        renderer.render(game)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(Direction.LEFT.offset)
                if event.key == pygame.K_UP:
                    game.move(Direction.UP.offset)
                if event.key == pygame.K_RIGHT:
                    game.move(Direction.RIGHT.offset)
                if event.key == pygame.K_DOWN:
                    game.move(Direction.DOWN.offset)
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    TICK_RATE -= 100
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    TICK_RATE += 100

        if game.gameover:
            print("GAMEOVER")
            print("step: {}".format(game.step))
            print("score: {}".format(game.score))
            q.put([game_counter, game.score])
            game_counter += 1
            game = Game1(SIZE)

        # TODO -> incapsulate to TimeSomething
        current_time = pygame.time.get_ticks()
        dt = current_time - timer
        if dt >= TICK_RATE:
            timer = current_time


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
