import pygame
import random
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np


class Game1:
    def __init__(self, size):
        from utils import Point
        self.size = size
        self.all_positions = [Point(i, j) for i in range(size) for j in range(size)]
        self.map = [[0 for i in range(size)] for j in range(size)]
        self.position = Point(size // 2, size // 2)
        self.food = self.init_food(self.position)
        self.score = 0
        self.step = 0
        self.gameover = False

    def init_food(self, position):
        food_test = self.all_positions.copy()
        food_test.remove(position)
        return random.choice(food_test)

    # TODO
    # def restart(self):
    #     pass

    def move(self, offset):
        self.step += 1
        if self.test_move(offset):
            self.position.move(offset)
            if self.position == self.food:
                self.score += 1
                self.food = self.init_food(self.position)
        else:
            self.gameover = True
        return not self.gameover

    def test_move(self, offset):
        t = self.position.copy()
        t.move(offset)
        return 0 <= t.x < self.size and 0 <= t.y < self.size


class Renderer:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (125, 125, 125)
    LIGHT_BLUE = (64, 128, 255)
    GREEN = (0, 200, 64)
    GREEN_DARK = (0, 255, 0)
    YELLOW = (225, 225, 0)
    PINK = (230, 50, 230)

    def __init__(self, surface, game_size):
        self.surface = surface

        self.width = surface.get_width()
        self.height = surface.get_height()

        self.columns = game_size[0]
        self.lines = game_size[1]

        self.cell_width = self.width / self.columns
        self.cell_height = self.height / self.lines

    def set_cell(self, color, column, line):
        pygame.draw.rect(self.surface, color, (column * self.cell_width,
                                               (self.lines - line) * self.cell_height - self.cell_height,
                                               self.cell_width, self.cell_height))

    def render(self, game):
        self.surface.fill((0, 0, 0))

        self.set_cell(Renderer.GREEN, game.position.x, game.position.y)
        self.set_cell(Renderer.YELLOW, game.food.x, game.food.y)

        # for column in range(game.size):
        #     for line in range(game.size):
        #         if game_map[column][line] != 0:
        #             self.set_cell(Renderer.GREEN, column, line)

        pygame.display.update()


class Agent:

    def __init__(self, column, lines):
        self.column = column
        self.lines = lines
        self.model = self.create_model()
        self.action_delta = 0.1

    def create_model():
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam()
        model.compile(loss='mse', optimizer=opt)
        return model

    def create_model():
        model = Sequential()
        model.add(LSTM(250, return_sequences=True))
        model.add(LSTM(250, return_sequences=True))
        model.add(Dropout(0.15))
        model.add(TimeDistributed(Dense(250)))
        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam()
        model.compile(loss='mse', optimizer=opt)
        return model

    def __calc_reward(self, state_old, state_new):
        if not state_old.gameover and state_new.gameover:
            return -100

        if state_old.score < state_new.score:
            return 10

        reward = 0

        if state_new.distance_to_feed < state_old.distance_to_feed:
            reward += 0.1

        if state_new.distance_to_feed > state_old.distance_to_feed:
            reward -= 0.1

        return reward

    def train(self, state_old, state_new, action):
        target_data = self.model.predict(state_old.data)
        target_data[0][list(Direction).index(action)] = self.__calc_reward(state_old, state_new)
        self.model.fit(state_old.data, target_data, epochs=1, verbose=0)

    def get_action(self, state):
        prediction = self.model.predict(state.data)[0]

        max_prediction = np.amax(prediction)
        delta = max_prediction * self.action_delta
        prediction_from = max_prediction - delta
        prediction_to = max_prediction + delta

        action_candidate_indices = np.where((prediction > prediction_from) & (prediction < prediction_to))[0]
        action_index = random.choice(action_candidate_indices)
        action = list(Direction)[action_index]

        return action


class State:

    def __init__(self, game):
        snake = game.snake
        head = game.snake.segments[0]
        food = game.food

        self.bool_state = np.array([
            snake.test_move(game.columns, game.lines, Direction.LEFT.shift),
            snake.test_move(game.columns, game.lines, Direction.UP.shift),
            snake.test_move(game.columns, game.lines, Direction.RIGHT.shift),
            snake.test_move(game.columns, game.lines, Direction.DOWN.shift),
            food.x < head.x,
            food.x > head.x,
            food.y < head.y,
            food.y < head.y,
        ])
        self.bool_state = 1*self.bool_state.reshape((1, self.bool_state.size))

        self.distance_to_feed = (head.x - game.food.x) ** 2 + (head.y - game.food.y) ** 2

        game_map = [[0 for i in range(game.columns)] for j in range(game.lines)]
        for seg in game.snake.segments:
            game_map[seg.x][seg.y] = 1

        game_map[head.x][head.y] = 2
        game_map[game.food.x][game.food.y] = 3
        result = np.rot90(np.array(game_map)).reshape((1, 400))
        # result = np.c_[np.rot90(np.array(map)).reshape((1, 400)), [self.distance_to_feed]]

        self.data = self.bool_state
        self.score = game.score
        self.gameover = game.gameover
