from game1 import Agent, Transition, QAgent


def main_game(q):
    import pygame
    import random
    from pygame.constants import QUIT
    from utils import Direction
    import numpy as np
    from game1 import Renderer
    from game1 import Game1

    TICK_RATE = 0
    WIDTH = 800
    HEIGHT = 800
    SIZE = 2
    EPSILON = 0.5

    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game1(SIZE)
    agent = QAgent(SIZE)
    renderer = Renderer(surface, (SIZE, SIZE))
    game_counter = 0

    # import pickle
    # with open('company_data.pkl', 'wb') as output:
    #     company1 = "Hellom World!"
    #     pickle.dump(company1, output, pickle.HIGHEST_PROTOCOL)
    #
    # with open('company_data.pkl', 'rb') as input:
    #     company1 = pickle.load(input)
    #     print(company1)

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
                if event.key == pygame.K_q:
                    EPSILON -= 0.1
                    print(EPSILON)
                if event.key == pygame.K_w:
                    EPSILON += 0.1
                    print(EPSILON)

        if game.gameover:
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

            if random.random() > EPSILON:
                a = agent.get_action(s1)
            else:
                a = random.choice(list(Direction))

            game.move(a.offset)
            r2 = game.score
            s2 = game.get_state()
            r = (r2 - r1) * 1  # TODO try cumulitive revard with step decrement
            if game.gameover:
                r = -1
            agent.remember(Transition(s1, s2, a, r))
            agent.train()
