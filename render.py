import pygame


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
