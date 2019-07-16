import matplotlib.pyplot as plt
from multiprocessing import Queue


def main_monitor(q: Queue):
    figure = plt.figure()
    handler = Handler()
    figure.canvas.mpl_connect('close_event', handler)

    plt.ion()
    plt.show()
    while not handler.closed:
        while not q.empty():
            numbers = q.get()
            plt.scatter(numbers[0], numbers[1])
        plt.pause(0.001)


class Handler:
    def __init__(self):
        self.closed = False

    def handle(self, event):
        self.closed = True

    def __call__(self, event):
        self.handle(event)
