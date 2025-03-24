import pygame

from read_file import read_constants

CONSTANTS = read_constants()


class Block:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width

        self.color = CONSTANTS["WHITE"]
        self.neighbors = []

        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def reset(self):
        self.color = CONSTANTS["WHITE"]

    def is_open(self):
        return self.color == CONSTANTS["GREEN"]

    def set_open(self):
        self.color = CONSTANTS["GREEN"]

    def is_closed(self):
        return self.color == CONSTANTS["RED"]

    def set_closed(self):
        self.color = CONSTANTS["RED"]

    def is_barrier(self):
        return self.color == CONSTANTS["BLACK"]

    def set_barrier(self):
        self.color = CONSTANTS["BLACK"]

    def is_start(self):
        return self.color == CONSTANTS["ORANGE"]

    def set_start(self):
        self.color = CONSTANTS["ORANGE"]

    def is_end(self):
        return self.color == CONSTANTS["PURPLE"]

    def set_end(self):
        self.color = CONSTANTS["PURPLE"]

    def set_path(self):
        self.color = CONSTANTS["TURQUOISE"]

    def is_neighbor(self, block):
        return block in self.neighbors

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < CONSTANTS["ROWS"] - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < CONSTANTS["ROWS"] - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
