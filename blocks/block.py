"""
Block class representing a single cell in the pathfinding grid.

Uses State Pattern to delegate behavior to state objects.
"""

import pygame
from typing import List, Tuple

# from config import constants
from blocks import block_state


class Block:
    """Single cell in the pathfinding grid with state-based behavior."""

    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows

        self._state = block_state.EMPTY
        self.neighbors: List['Block'] = []

    @property
    def state(self) -> block_state.BlockState:
        """Get current state."""
        return self._state

    def set_state(self, new_state: block_state.BlockState) -> bool:
        """
        Change block state with validation.
        Returns True if transition succeeded, False if invalid.
        """
        if self._state.can_transition_to(new_state):
            self._state = new_state
            return True
        return False

    def reset(self) -> None:
        """Reset to empty state."""
        self._state = block_state.EMPTY

    def is_empty(self) -> bool:
        return isinstance(self._state, block_state.EmptyState)

    def is_barrier(self) -> bool:
        return isinstance(self._state, block_state.BarrierState)

    def set_barrier(self) -> None:
        self.set_state(block_state.BARRIER)

    def is_start(self) -> bool:
        return isinstance(self._state, block_state.StartState)

    def set_start(self) -> None:
        self.set_state(block_state.START)

    def is_end(self) -> bool:
        return isinstance(self._state, block_state.EndState)

    def set_end(self) -> None:
        self.set_state(block_state.END)

    def is_open(self) -> bool:
        return isinstance(self._state, block_state.OpenState)

    def set_open(self) -> None:
        self.set_state(block_state.OPEN)

    def is_closed(self) -> bool:
        return isinstance(self._state, block_state.ClosedState)

    def set_closed(self) -> None:
        self.set_state(block_state.CLOSED)

    def set_path(self) -> None:
        self.set_state(block_state.PATH)

    def is_walkable(self) -> bool:
        """Can pathfinding traverse this block?"""
        return self._state.is_walkable()

    def draw(self, window: pygame.Surface) -> None:
        """Render block to pygame surface."""
        color = self._state.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, self.width, self.width))

    def get_position(self) -> Tuple[int, int]:
        """Return (row, col) position."""
        return self.row, self.col

    def update_neighbors(self, grid: List[List['Block']]) -> None:
        """Update list of walkable neighbors (up, down, left, right)."""
        self.neighbors = []

        # Down
        if self.row < self.total_rows - 1:
            neighbor = grid[self.row + 1][self.col]
            if neighbor.is_walkable():
                self.neighbors.append(neighbor)

        # Up
        if self.row > 0:
            neighbor = grid[self.row - 1][self.col]
            if neighbor.is_walkable():
                self.neighbors.append(neighbor)

        # Right
        if self.col < self.total_rows - 1:
            neighbor = grid[self.row][self.col + 1]
            if neighbor.is_walkable():
                self.neighbors.append(neighbor)

        # Left
        if self.col > 0:
            neighbor = grid[self.row][self.col - 1]
            if neighbor.is_walkable():
                self.neighbors.append(neighbor)

    def is_neighbor(self, block: 'Block') -> bool:
        """Check if block is a neighbor."""
        return block in self.neighbors

    def __repr__(self) -> str:
        return f"Block({self.row}, {self.col}, state={self._state})"

    def __lt__(self, other: 'Block') -> bool:
        """For priority queue compatibility."""
        return False