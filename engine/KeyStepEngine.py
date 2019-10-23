import pygame
from pygame.constants import QUIT


class KeyStepEngine:
    def __init__(self, game, handler, renderer):
        self.game = game
        self.handler = handler
        self.renderer = renderer

    def run(self):
        while True:
            self.renderer.render(self.game)
            self.handle_input_event()
            self.handler.operate(self.game, self)
            if self.game.game_over:
                self.handler.on_game_over(self.game, self)

    def handle_input_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                self.handler.on_key(self.game, self, event.key)


class KeyStepEngineHandler:
    def operate(self, game, engine):
        raise NotImplementedError

    def on_key(self, game, engine, key):
        raise NotImplementedError

    def on_game_over(self, game, engine):
        raise NotImplementedError


