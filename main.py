import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process, Queue
import multiprocessing as mp

from Direction import Direction
from Game1 import Game1

TICK_RATE = 100

WIDTH = 800
HEIGHT = 800

MAIN_MONITOR_CLOSED = False


def handle_close(evt):
    global MAIN_MONITOR_CLOSED
    MAIN_MONITOR_CLOSED = True


def main_monitor(q):
    figure = plt.figure()
    figure.canvas.mpl_connect('close_event', handle_close)

    plt.ion()
    plt.show()
    while not MAIN_MONITOR_CLOSED:
        while not q.empty():
            numbers = q.get()
            x = np.random.random()
            y = np.random.random()
            plt.scatter(x, y)
        plt.pause(0.001)


def main_game(q):
    global TICK_RATE
    global WIDTH
    global HEIGHT

    SIZE = 3

    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game1(SIZE)
    # TODO renderer = SurfaceBlockRenderer(surface, size, size)

    timer = pygame.time.get_ticks()
    while True:
        # render begin
        surface.fill((0, 0, 0))

        pygame.display.update()
        # render end

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                q.put([1, 2, 3, 4, 5, 6, 7, 8, 9])
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

        # TODO -> incapsulate to TimeSomething
        current_time = pygame.time.get_ticks()
        dt = current_time - timer
        if dt >= TICK_RATE:
            timer = current_time


if __name__ == "__main__":
    mp.set_start_method("spawn")

    queue = Queue()

    p1 = Process(target=main_game, args=[queue])
    p1.start()

    p2 = Process(target=main_monitor, args=[queue])
    p2.start()

    p1.join()
    p2.join()
