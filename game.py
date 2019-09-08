from engine.KeyStepEngine import KeyStepEngine
from game1 import Agent, Transition, QAgent
import pygame
import copy
from utils import Direction, Point
from game1 import Renderer
from game1 import Game1


class KeyStepEngineHandler:
    def __init__(self, agent):
        self.agent = agent

    def on_step(self, game, engine, key):
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
            r1 = game.score
            s1 = game.get_state()

            a = self.agent.get_action(s1)

            game.move(a.offset)

            r2 = game.score
            s2 = game.get_state()

            k_positive = 1  # Коэффициент положительного подкрепления
            k_negative = 10  # Коэффициент отрицательного подкрепления

            r = (r2 - r1) * k_positive + 1
            if game.game_over:
                r = -1 * k_negative

            t = Transition(s1, s2, a, r)

            print("score: " + str(game.score))

            # self.agent.remember(t)
            # self.agent.train()
            # self.agent.train2(t)

    def on_game_over(self, game, engine):
        game.restart()


class Operator:
    def __init__(self, agent):
        self.agent = agent

    def get_action(self):
        pass


class AgentOperator:
    def __init__(self, agent):
        self.agent = agent

    def get_action(self):
        pass


class HumanOperator:
    def __init__(self):
        self.stub = "stub"

    def get_action(self):
        pass


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


def main_game(q):
    WIDTH = 800
    HEIGHT = 800
    SIZE = 4

    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    renderer = Renderer(surface, (SIZE, SIZE))
    game = Game1(SIZE)
    agent = QAgent(SIZE)
    handler = KeyStepEngineHandler(agent)

    transitions = generate_transitions(SIZE)
    for t in transitions:
        agent.remember(t)

    for i in range(2000):
        print(i)
        agent.train()

    engine = KeyStepEngine(game, handler, renderer)
    engine.run()
