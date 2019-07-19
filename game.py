from game1 import Agent, Transition, QAgent


def main_game(q):
    import pygame
    from pygame.constants import QUIT
    from utils import Direction
    import numpy as np
    from game1 import Renderer
    from game1 import Game1

    TICK_RATE = 50
    WIDTH = 800
    HEIGHT = 800
    SIZE = 4

    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game1(SIZE)
    agent = QAgent()
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

            r1 = game.score
            s1 = game.get_state()
            a = agent.get_action(s1)
            game.move(a.offset)
            r2 = game.score
            s2 = game.get_state()
            r = (r2 - r1) * 20  # TODO try cumulitive revard with step decrement
            agent.remember(Transition(s1, s2, a, r))
            agent.train()
