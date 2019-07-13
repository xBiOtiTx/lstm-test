import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue, JoinableQueue

from keras.utils import plot_model

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
                # plot_model(agent.model, to_file='model.png')
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    q.put([1, 2, 3, 4, 5, 6, 7, 8, 9])
                    print("left")
                    # game.move(Direction.LEFT.offset)
                if event.key == pygame.K_UP:
                    q.put([9, 8, 7, 6, 5, 4, 3, 2, 1])
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


if __name__ == "__main__":
    queue = Queue()

    p1 = Process(target=main_game, args=[queue])
    p1.start()

    p2 = Process(target=main_monitor, args=[queue])
    p2.start()

    p1.join()
    p2.join()
    # main_game()
