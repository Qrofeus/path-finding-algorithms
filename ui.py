import pygame

from block import Block
from read_file import read_constants

CONSTANTS = read_constants()


def get_mouse_pos():
    gap = CONSTANTS["WIDTH"] // CONSTANTS["ROWS"]
    y, x = pygame.mouse.get_pos()

    row = y // gap
    col = x // gap

    return row, col


def make_grid():
    grid = []
    gap = CONSTANTS["WIDTH"] // CONSTANTS["ROWS"]
    for i in range(CONSTANTS["ROWS"]):
        grid.append([])
        for j in range(CONSTANTS["ROWS"]):
            grid[i].append(Block(i, j, gap, CONSTANTS["ROWS"]))
    return grid


def highlight_path(trace, block, window_update_func):
    while block in trace:
        block = trace[block]
        block.set_path()
        window_update_func()


class PygameWindow:
    def __init__(self):
        self.window = pygame.display.set_mode((CONSTANTS["WIDTH"], CONSTANTS["WIDTH"]))
        pygame.display.set_caption("A* Path Finding")

    def draw_grid(self):
        gap = CONSTANTS["WIDTH"] // CONSTANTS["ROWS"]
        for i in range(CONSTANTS["ROWS"]):
            pygame.draw.line(self.window, CONSTANTS["GREY"], (0, i * gap), (CONSTANTS["WIDTH"], i * gap))

        for j in range(CONSTANTS["ROWS"]):
            pygame.draw.line(self.window, CONSTANTS["GREY"], (j * gap, 0), (j * gap, CONSTANTS["WIDTH"]))

    def update(self, grid):
        self.window.fill(CONSTANTS["BLACK"])
        for row in grid:
            for block in row:
                block.draw(self.window)

        self.draw_grid()
        pygame.display.update()
