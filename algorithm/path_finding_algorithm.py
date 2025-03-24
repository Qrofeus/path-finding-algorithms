from abc import ABC, abstractmethod


class PathFindingAlgorithm(ABC):
    @abstractmethod
    def run(self, grid, start_block, end_block, window_update_func):
        """Runs the pathfinding algorithm and returns the shortest path."""
        pass

    @abstractmethod
    def get_distance(self, block1, block2):
        """Calculates the heuristic distance between two blocks."""
        pass
