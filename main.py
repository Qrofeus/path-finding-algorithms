import pygame
from queue import PriorityQueue
from CONSTANTS import ROWS, WIDTH, COLOR

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding")


class Block:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width

        self.color = COLOR["WHITE"]
        self.neighbors = []

        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def reset(self):
        self.color = COLOR["WHITE"]

    def is_open(self):
        return self.color == COLOR["GREEN"]

    def set_open(self):
        self.color = COLOR["GREEN"]

    def is_closed(self):
        return self.color == COLOR["RED"]

    def set_closed(self):
        self.color = COLOR["RED"]

    def is_barrier(self):
        return self.color == COLOR["BLACK"]

    def set_barrier(self):
        self.color = COLOR["BLACK"]

    def is_start(self):
        return self.color == COLOR["ORANGE"]

    def set_start(self):
        self.color = COLOR["ORANGE"]

    def is_end(self):
        return self.color == COLOR["PURPLE"]

    def set_end(self):
        self.color = COLOR["PURPLE"]

    def set_path(self):
        self.color = COLOR["TURQUOISE"]

    def is_neighbor(self, block):
        return block in self.neighbors

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(block1, block2):
    # Manhattan Distance
    return abs(block1[0] - block2[0]) + abs(block1[1] - block2[1])


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Block(i, j, gap, rows))
    return grid


def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, COLOR["GREY"], (0, i * gap), (width, i * gap))

    for j in range(rows):
        pygame.draw.line(window, COLOR["GREY"], (j * gap, 0), (j * gap, width))


def update_board(window, grid, rows, width):
    window.fill(COLOR["BLACK"])
    for row in grid:
        for block in row:
            block.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def get_mouse_pos(rows, width):
    gap = width // rows
    y, x = pygame.mouse.get_pos()

    row = y // gap
    col = x // gap

    return row, col


def highlight_path(came_from, block, update_window_func):
    while block in came_from:
        block = came_from[block]
        block.set_path()
        update_window_func()


def algorithm(update_window_func, grid, start_block: Block, end_block: Block):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_block))
    came_from = {}

    g_score = {block: float("inf") for row in grid for block in row}
    g_score[start_block] = 0

    f_score = {block: float("inf") for row in grid for block in row}
    f_score[start_block] = h(start_block.get_position(), end_block.get_position())

    open_set_hash = {start_block}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end_block:
            highlight_path(came_from, end_block, update_window_func)
            start_block.set_start()
            end_block.set_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end_block.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()

        update_window_func()
        if current != start_block:
            current.set_closed()

    return False


def main(window, width):
    grid = make_grid(ROWS, width)

    start_position = None
    end_position = None

    running = True

    while running:
        update_board(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if pygame.mouse.get_pressed()[0]:
                # LEFT CLICK
                row, col = get_mouse_pos(ROWS, width)
                block = grid[row][col]

                if not start_position and block != end_position:
                    block.set_start()
                    start_position = block
                    continue

                if not end_position and block != start_position:
                    block.set_end()
                    end_position = block
                    continue

                if block != start_position and block != end_position:
                    block.set_barrier()

            elif pygame.mouse.get_pressed()[2]:
                # RIGHT CLICK
                row, col = get_mouse_pos(ROWS, width)

                block = grid[row][col]
                if block.is_start():
                    start_position = None
                if block.is_end():
                    end_position = None
                block.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_position and end_position:
                    for row in grid:
                        for block in row:
                            block.update_neighbors(grid)

                    algorithm(lambda: update_board(window, grid, ROWS, width), grid, start_position, end_position)

                if event.key == pygame.K_c:
                    start_position = None
                    end_position = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == '__main__':
    main(WINDOW, WIDTH)
