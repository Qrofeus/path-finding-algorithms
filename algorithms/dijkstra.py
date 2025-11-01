"""
Dijkstra's pathfinding algorithm implementation.

Uses g(n) = cost from start to n (no heuristic).
Explores all directions equally, guarantees shortest path.
"""

from queue import PriorityQueue
from typing import List, Dict
from blocks.block import Block
from algorithms.base_pathfinder import BasePathfinder, PathfindingResult


class DijkstraPathfinder(BasePathfinder):
    """Dijkstra's algorithm - uniform cost search without heuristic."""

    def find_path(self, grid: List[List[Block]], start: Block, end: Block) -> PathfindingResult:
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))

        came_from: Dict[Block, Block] = {}
        g_score = {block: float("inf") for row in grid for block in row}
        g_score[start] = 0

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

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((g_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

        return PathfindingResult(None, came_from, visited)