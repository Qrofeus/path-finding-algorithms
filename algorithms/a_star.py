"""
A* pathfinding algorithm implementation.

Uses f(n) = g(n) + h(n) where:
- g(n) = cost from start to n
- h(n) = heuristic estimate from n to goal
"""

from queue import PriorityQueue
from typing import List, Dict
from blocks.block import Block
from algorithms.base_pathfinder import BasePathfinder, PathfindingResult


class AStarPathfinder(BasePathfinder):
    """A* pathfinding algorithm with heuristic optimization."""

    def find_path(self, grid: List[List[Block]], start: Block, end: Block) -> PathfindingResult:
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))

        came_from: Dict[Block, Block] = {}
        g_score = {block: float("inf") for row in grid for block in row}
        g_score[start] = 0

        f_score = {block: float("inf") for row in grid for block in row}
        f_score[start] = self.manhattan_distance(start.get_position(), end.get_position())

        open_set_hash = {start}
        visited = []

        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                path = self.reconstruct_path(came_from, end)
                return PathfindingResult(path, came_from, visited)

            visited.append(current)

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.manhattan_distance(
                        neighbor.get_position(), end.get_position()
                    )

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

        return PathfindingResult(None, came_from, visited)