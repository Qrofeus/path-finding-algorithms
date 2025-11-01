"""
Base class for pathfinding algorithms using Strategy Pattern.

Separates algorithm logic from visualization concerns.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from blocks.block import Block


class PathfindingResult:
    """Container for pathfinding algorithm results."""

    def __init__(self, path: Optional[List[Block]], came_from: Dict[Block, Block], visited: List[Block]):
        self.path = path
        self.came_from = came_from
        self.visited = visited
        self.found = path is not None

    def get_path_length(self) -> int:
        return len(self.path) if self.path else 0


class BasePathfinder(ABC):
    """Abstract base class for pathfinding algorithms."""

    def __init__(self):
        self.came_from: Dict[Block, Block] = {}
        self.visited: List[Block] = []

    @abstractmethod
    def find_path(self, grid: List[List[Block]], start: Block, end: Block) -> PathfindingResult:
        """
        Find path from start to end.

        Args:
            grid: 2D list of blocks
            start: Starting block
            end: Goal block

        Returns:
            PathfindingResult containing path and metadata
        """
        pass

    def reconstruct_path(self, came_from: Dict[Block, Block], current: Block) -> List[Block]:
        """Reconstruct path from came_from dictionary."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance heuristic."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])