import pygame
from pygame.constants import QUIT


class TimeHandler:
    def __init__(self):
        pass

    def register(self):
        pass

    def unregister(self):
        pass


class TimeStepEngine:
    def __init__(self, game, handler, renderer):
        self.game = game
        self.handler = handler
        self.renderer = renderer
        # self.actions_per_step = 10
        self.steps_per_second = 1
        self.step_rate = 1000 / self.steps_per_second

    def run(self):
        old_time = pygame.time.get_ticks()
        while True:
            self.renderer.render(self.game)
            self.handle_input_event()
            # self.operator.act(self.game)
            if self.game.game_over:
                self.handler.on_game_over()
            # else
            current_time = pygame.time.get_ticks()
            dt = current_time - old_time
            if dt >= self.step_rate:
                old_time = current_time
                self.handler.on_step(self.game, self)

    def handle_input_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                self.handler.on_key(event.key)


class TimeStepEngineHandler:
    def on_key(self, game, engine, key):
        raise NotImplementedError

    def on_step(self, game, engine):
        raise NotImplementedError

    def on_game_over(self, game, engine):
        raise NotImplementedError
