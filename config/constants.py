"""Configuration constants for pathfinding visualizer."""

from typing import Tuple

# Display settings
WIDTH: int = 800
ROWS: int = 50
GAP: int = WIDTH // ROWS

# Colors (RGB)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
PURPLE: Tuple[int, int, int] = (128, 0, 128)
ORANGE: Tuple[int, int, int] = (255, 165, 0)
GREY: Tuple[int, int, int] = (128, 128, 128)
TURQUOISE: Tuple[int, int, int] = (64, 224, 208)