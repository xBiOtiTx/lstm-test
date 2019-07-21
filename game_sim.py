from game1 import Agent, Transition, QAgent


def main_game_sim(q):
    import random
    from utils import Direction
    import numpy as np
    import pickle
    from game1 import Game1

    SIZE = 2
    GAME_COUNT_MAX = 1000
    TRAIN_COUNT_MAX = 100

    game = Game1(SIZE)
    agent = QAgent(SIZE)
    game_counter = 0
    total_score = 0

    transitions = None
    with open('transitions2x2.pkl', 'rb') as input:
        transitions = pickle.load(input)

    # bad = []
    # for t in transitions:
    #     if len(t.s1) != 9 or len(t.s2) != 9:
    #         bad.append(t)
    #
    # for b in bad:
    #     transitions.remove(b)

    agent.transitions = transitions

    for i in range(TRAIN_COUNT_MAX):
        print("Train: {} of {} is over".format(i, TRAIN_COUNT_MAX))
        agent.train()

    while game_counter < GAME_COUNT_MAX:
        # while True:
        a = agent.get_action(game.get_state())
        # a = random.choice(list(Direction))
        game.move(a.offset)

        # r1 = game.score
        # s1 = game.get_state()
        # a = random.choice(list(Direction))
        # game.move(a.offset)
        # r2 = game.score
        # s2 = game.get_state()
        # r = (r2 - r1) * 1
        # if game.gameover:
        #     r = -1
        # agent.remember(Transition(s1, s2, a, r))

        if game.gameover:
            q.put([game_counter, game.score])
            game_counter += 1
            total_score += game.score
            print("Game: {} of {} is over".format(game_counter, GAME_COUNT_MAX))
            game = Game1(SIZE)

    print("Average score: {}".format(total_score / game_counter))
