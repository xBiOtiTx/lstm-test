import pygame
from pygame.locals import *

from keras.utils import plot_model

TICK_RATE = 100

WIDTH = 800
HEIGHT = 800

if __name__ == "__main__":

    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))

    timer = pygame.time.get_ticks()
    while True:
        # render begin
        surface.fill((0, 0, 0))

        pygame.display.update()
        # render end

        for event in pygame.event.get():
            if event.type == QUIT:
                plot_model(agent.model, to_file='model.png')
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("left")
                    # game.move(Direction.LEFT.offset)
                if event.key == pygame.K_UP:
                    print("up")
                    # game.rotate()
                if event.key == pygame.K_RIGHT:
                    print("right")
                    # game.move(Direction.RIGHT.offset)
                if event.key == pygame.K_DOWN:
                    print("down")
                    # game.move(Direction.DOWN.offset)
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    TICK_RATE -= 100
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    TICK_RATE += 100

        # TODO -> incapsulate to TimeSomething
        current_time = pygame.time.get_ticks()
        dt = current_time - timer
        if dt >= TICK_RATE:
            timer = current_time
