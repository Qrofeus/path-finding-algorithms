"""
Wilson's Algorithm for unbiased maze generation.

Generates mazes by performing loop-erased random walks.
Every possible maze has equal probability of being generated.
"""

import random
from typing import List
from blocks.block import Block


class WilsonMazeGenerator:
    """Generates perfect mazes using Wilson's algorithm."""

    def __init__(self):
        self.path: List[Block] = []

    def generate(self, grid: List[List[Block]]) -> None:
        """
        Generate maze by carving paths and adding barriers.

        Process:
        1. Mark all blocks as closed (unvisited)
        2. Pick random target, set to empty
        3. Start from random closed block, walk until hitting empty
        4. Add barriers around path
        5. Repeat until no closed blocks remain
        """
        # Initialize all blocks as closed (unvisited)
        for row in grid:
            for block in row:
                block.set_closed()

        unvisited = self._get_unvisited_blocks(grid)

        while unvisited:
            # Pick random target from closed blocks and set to empty
            target = random.choice(unvisited)
            target.reset()

            # Update unvisited after setting target
            unvisited = self._get_unvisited_blocks(grid)
            if not unvisited:
                break

            # Start walk from random unvisited block
            current = random.choice(unvisited)
            path, reached = self._random_walk(grid, current, target)

            # If target was not reached, convert it back to closed
            if not reached and target.is_empty():
                target.set_closed()

            # Add barriers around path (only on closed neighbors)
            self._add_barriers_around_path(grid, path)

            unvisited = self._get_unvisited_blocks(grid)

        # Convert any remaining closed blocks to barriers
        for row in grid:
            for block in row:
                if block.is_closed():
                    block.set_barrier()

    def _random_walk(self, grid: List[List[Block]], start: Block, target: Block) -> tuple:
        """
        Perform loop-erased random walk and return the path and whether target was reached.

        Returns:
            (path, reached): path is list of blocks, reached is True if we hit an empty block
        """
        self.path = [start]
        current = start
        reached = False

        steps = 0
        max_steps = len(grid) * 3  # Safety limit

        # Walk until we hit an empty block
        while True:
            steps += 1
            if steps > max_steps:
                break

            neighbors = self._get_closed_neighbors(grid, current)
            if not neighbors:
                # No more closed blocks to walk through
                # Check if we're adjacent to an empty block (reached target)
                empty_neighbors = self._get_empty_neighbors(grid, current)
                if empty_neighbors:
                    reached = True
                break

            next_block = random.choice(neighbors)

            if next_block in self.path:
                # Loop detected - erase it by resetting back to closed
                loop_index = self.path.index(next_block)
                for block in self.path[loop_index + 1:]:
                    # Only set back to closed if it's currently empty
                    if block.is_empty():
                        block.set_closed()
                self.path = self.path[:loop_index + 1]
                current = next_block
            else:
                # Add to path and mark as empty
                next_block.reset()
                self.path.append(next_block)
                current = next_block

        return self.path.copy(), reached

    def _add_barriers_around_path(self, grid: List[List[Block]], path: List[Block]) -> None:
        """Add barriers around the path by converting closed neighbors to barriers."""
        for block in path:
            neighbors = self._get_closed_neighbors(grid, block)
            for neighbor in neighbors:
                neighbor.set_barrier()

    def _get_closed_neighbors(self, grid: List[List[Block]], block: Block) -> List[Block]:
        """Get neighbors that are closed (unvisited only)."""
        neighbors = []
        row, col = block.get_position()
        total_rows = len(grid)
        total_cols = len(grid[0]) if grid else 0

        if row > 0:
            neighbor = grid[row - 1][col]
            if neighbor.is_closed():
                neighbors.append(neighbor)
        if row < total_rows - 1:
            neighbor = grid[row + 1][col]
            if neighbor.is_closed():
                neighbors.append(neighbor)
        if col > 0:
            neighbor = grid[row][col - 1]
            if neighbor.is_closed():
                neighbors.append(neighbor)
        if col < total_cols - 1:
            neighbor = grid[row][col + 1]
            if neighbor.is_closed():
                neighbors.append(neighbor)

        return neighbors

    def _get_empty_neighbors(self, grid: List[List[Block]], block: Block) -> List[Block]:
        """Get neighbors that are empty."""
        neighbors = []
        row, col = block.get_position()
        total_rows = len(grid)
        total_cols = len(grid[0]) if grid else 0

        if row > 0:
            neighbor = grid[row - 1][col]
            if neighbor.is_empty():
                neighbors.append(neighbor)
        if row < total_rows - 1:
            neighbor = grid[row + 1][col]
            if neighbor.is_empty():
                neighbors.append(neighbor)
        if col > 0:
            neighbor = grid[row][col - 1]
            if neighbor.is_empty():
                neighbors.append(neighbor)
        if col < total_cols - 1:
            neighbor = grid[row][col + 1]
            if neighbor.is_empty():
                neighbors.append(neighbor)

        return neighbors

    def _get_unvisited_blocks(self, grid: List[List[Block]]) -> List[Block]:
        """Get blocks that are still closed (unvisited). Only closed blocks count."""
        unvisited = []
        for row in grid:
            for block in row:
                if block.is_closed():
                    unvisited.append(block)
        return unvisited

    def clear(self) -> None:
        """Reset generator state."""
        self.path.clear()