import matplotlib.pyplot as plt
from multiprocessing import Queue
import time


def main_monitor(q: Queue):
    figure = plt.figure()
    handler = Handler()
    figure.canvas.mpl_connect('close_event', handler)

    points_x = []
    points_y = []
    plt.ion()
    plt.show()
    timer = time.time()
    while not handler.closed:
        while not q.empty():
            numbers = q.get()
            points_x.append(numbers[0])
            points_y.append(numbers[1])
            if len(points_x) > 1000:
                del points_x[1::2]
                del points_y[1::2]
            # plt.scatter(numbers[0], numbers[1])

        current_time = time.time()
        dt = current_time - timer
        if dt > 1:
            timer = time.time()
            plt.cla()
            plt.plot(points_x, points_y)
        plt.pause(0.001)


class Handler:
    def __init__(self):
        self.closed = False

    def handle(self, event):
        self.closed = True

    def __call__(self, event):
        self.handle(event)
