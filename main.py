from multiprocessing import Process, Queue
import multiprocessing as mp
from game import main_game
from game_sim import main_game_sim
from monitoring import main_monitor


if __name__ == "__main__":
    mp.set_start_method("spawn")

    queue = Queue()

    # p1 = Process(target=main_game, args=[queue])
    # p1.start()

    p1 = Process(target=main_game_sim, args=[queue])
    p1.start()

    p2 = Process(target=main_monitor, args=[queue])
    p2.start()

    p1.join()
    p2.join()
