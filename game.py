from engine.KeyStepEngine import KeyStepEngine
from game1 import Agent, Transition, QAgent
import pygame
from utils import Direction, Point
from game1 import Renderer
from game1 import Game1


class KeyStepEngineHandler:
    def __init__(self, agent):
        self.agent = agent

    def operate(self, game, engine):
        pass

    def on_key(self, game, engine, key):
        a = None
        if key == pygame.K_LEFT:
            a = Direction.LEFT
        if key == pygame.K_UP:
            a = Direction.UP
        if key == pygame.K_RIGHT:
            a = Direction.RIGHT
        if key == pygame.K_DOWN:
            a = Direction.DOWN

        if a is not None:
            game.move(a.offset)
            print("score: " + str(game.score))

    def on_game_over(self, game, engine):
        game.restart()


class AgentHandler:
    def __init__(self, agent, train=False):
        self.agent = agent
        self.train = train

    def operate(self, game, engine):
        r1 = game.score
        s1 = game.get_state()

        a = self.agent.get_action(s1)

        game.move(a.offset)

        r2 = game.score
        s2 = game.get_state()

        k_positive = 1  # Коэффициент положительного подкрепления
        k_negative = 1  # Коэффициент отрицательного подкрепления

        r = (r2 - r1) * k_positive
        if game.game_over:
            r = -1 * k_negative

        t = Transition(s1, s2, a, r)

        print("score: " + str(game.score))

        if self.train:
            self.agent.remember(t)
            self.agent.train()

    def on_key(self, game, engine, key):
        pass

    def on_game_over(self, game, engine):
        game.restart()


def generate_transitions(size):
    game = Game1(size)
    transitions = []
    for h_i in range(size):
        for h_j in range(size):
            head = Point(h_i, h_j)
            for f_i in range(size):
                for f_j in range(size):
                    if h_i != f_i or h_j != f_j:
                        food = Point(f_i, f_j)
                        for a in list(Direction):
                            game.init(head, food)
                            r1 = game.score
                            s1 = game.get_state()
                            game.move(a.offset)
                            r2 = game.score
                            s2 = game.get_state()
                            r = (r2 - r1) * 10
                            if game.game_over:
                                r = -1
                            t = Transition(s1, s2, a, r)
                            transitions.append(t)
    return transitions


class GameSimulator:
    def run(self):
        for size in range(10, 20):
            self.inner_success(size)

    # def inner_success(self, size):
    #     transitions = generate_transitions(size)
    #
    #     for layers in range(1, 10):
    #         for units in range(4, 10, 8):
    #             for trains in range(500, 10000, 500):
    #                 agent = QAgent(size, layers, 2**units)
    #                 for t in transitions:
    #                     agent.remember(t)
    #                 for i in range(trains):
    #                     agent.train()
    #
    #                 if self.success(size, agent):
    #                     print((size, layers, 2**units, trains, "SUCCESS"))
    #                     return
    #                 else:
    #                     print((size, layers, 2**units, trains, "FAIL"))

    def inner_success(self, size):
        transitions = generate_transitions(size)
        trains = 10000

        for layers in range(1, 5):
            for units in range(9, 13):
                agent = QAgent(size, layers, 2**units)
                for t in transitions:
                    agent.remember(t)
                for i in range(trains):
                    agent.train()

                if self.success(size, agent):
                    print((size, layers, 2**units, trains, "SUCCESS"))
                    return
                else:
                    print((size, layers, 2**units, trains, "FAIL"))

    def success(self, size, agent):
        attempts = 10
        wrong_route = size * size * 2
        target_score = 50
        game = Game1(size)
        max_score = 0
        for attempt in range(attempts):
            while not game.game_over:
                a = agent.get_action(game.get_state())
                game.move(a.offset)
                max_score = max(max_score, game.score)
                if game.last_step >= wrong_route:
                    break
                if game.score >= target_score:
                    return True
            game.restart()
        return False


def main_game(q):
    g = GameSimulator()
    g.run()
    # WIDTH = 800
    # HEIGHT = 800
    # SIZE = 5
    #
    # pygame.init()
    # surface = pygame.display.set_mode((WIDTH, HEIGHT))
    # renderer = Renderer(surface, (SIZE, SIZE))
    # game = Game1(SIZE)
    # agent = QAgent(SIZE)
    # handler = AgentHandler(agent)
    #
    # transitions = generate_transitions(SIZE)
    # for t in transitions:
    #     agent.remember(t)
    #
    # for i in range(3000):
    #     print(i)
    #     agent.train()
    #
    # engine = KeyStepEngine(game, handler, renderer)
    # engine.run()
