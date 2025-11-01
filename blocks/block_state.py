"""
State Pattern implementation for block behaviors.

Each block state encapsulates its own rendering and pathfinding properties.
States validate their own transitions to prevent invalid state changes.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

from config import constants

if TYPE_CHECKING:
    from blocks.block import Block


class BlockState(ABC):
    """Abstract base class for all block states."""

    @abstractmethod
    def get_color(self) -> Tuple[int, int, int]:
        """Return the color to render this state."""
        pass

    @abstractmethod
    def is_walkable(self) -> bool:
        """Can pathfinding algorithms traverse this block?"""
        pass

    @abstractmethod
    def can_transition_to(self, new_state: 'BlockState') -> bool:
        """Validate if transition to new_state is allowed."""
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__


class EmptyState(BlockState):
    """Default state - unvisited, walkable block."""

    def get_color(self) -> Tuple[int, int, int]:
        return constants.WHITE

    def is_walkable(self) -> bool:
        return True

    def can_transition_to(self, new_state: BlockState) -> bool:
        return True


class BarrierState(BlockState):
    """Wall that blocks pathfinding."""

    def get_color(self) -> Tuple[int, int, int]:
        return constants.BLACK

    def is_walkable(self) -> bool:
        return False

    def can_transition_to(self, new_state: BlockState) -> bool:
        return isinstance(new_state, (EmptyState, BarrierState))


class StartState(BlockState):
    """Starting point for pathfinding."""

    def get_color(self) -> Tuple[int, int, int]:
        return constants.ORANGE

    def is_walkable(self) -> bool:
        return True

    def can_transition_to(self, new_state: BlockState) -> bool:
        return isinstance(new_state, (EmptyState, StartState))


class EndState(BlockState):
    """Goal point for pathfinding."""

    def get_color(self) -> Tuple[int, int, int]:
        return constants.PURPLE

    def is_walkable(self) -> bool:
        return True

    def can_transition_to(self, new_state: BlockState) -> bool:
        return isinstance(new_state, (EmptyState, EndState))


class OpenState(BlockState):
    """Blocks in the algorithms's open set (discovered but not fully explored)."""

    def get_color(self) -> Tuple[int, int, int]:
        return constants.GREEN

    def is_walkable(self) -> bool:
        return True

    def can_transition_to(self, new_state: BlockState) -> bool:
        return isinstance(new_state, (ClosedState, PathState, EmptyState, OpenState))


class ClosedState(BlockState):
    """Blocks in the algorithms's closed set (fully explored)."""

    def get_color(self) -> Tuple[int, int, int]:
        return constants.RED

    def is_walkable(self) -> bool:
        return True

    def can_transition_to(self, new_state: BlockState) -> bool:
        return isinstance(new_state, (PathState, EmptyState, ClosedState, BarrierState))


class PathState(BlockState):
    """Final path from start to end."""

    def get_color(self) -> Tuple[int, int, int]:
        return constants.TURQUOISE

    def is_walkable(self) -> bool:
        return True

    def can_transition_to(self, new_state: BlockState) -> bool:
        return isinstance(new_state, (EmptyState, PathState))


# Singleton instances
EMPTY = EmptyState()
BARRIER = BarrierState()
START = StartState()
END = EndState()
OPEN = OpenState()
CLOSED = ClosedState()
PATH = PathState()