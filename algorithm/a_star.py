from queue import PriorityQueue

import pygame

from algorithm.path_finding_algorithm import PathFindingAlgorithm
from block import Block
from ui import highlight_path


class AStar(PathFindingAlgorithm):
    def __init__(self):
        super().__init__()

    def get_distance(self, block1_position, block2_position):
        # Manhattan Distance
        return abs(block1_position[0] - block2_position[0]) + abs(block1_position[1] - block2_position[1])

    def run(self, grid, start_block: Block, end_block: Block, window_update_func):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start_block))
        came_from = {}

        g_score = {block: float("inf") for row in grid for block in row}
        g_score[start_block] = 0

        f_score = {block: float("inf") for row in grid for block in row}
        f_score[start_block] = self.get_distance(start_block.get_position(), end_block.get_position())

        open_set_hash = {start_block}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end_block:
                highlight_path(came_from, end_block, window_update_func)
                start_block.set_start()
                end_block.set_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.get_distance(neighbor.get_position(), end_block.get_position())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.set_open()

            window_update_func()
            if current != start_block:
                current.set_closed()

        return False
