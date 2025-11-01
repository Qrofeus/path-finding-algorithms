"""
Visualization layer for pathfinding algorithms.

Handles pygame rendering and animation separate from main logic.
"""

import pygame
from typing import List, Optional, Tuple
from blocks.block import Block
from config import constants
from algorithms.base_pathfinder import PathfindingResult


class PathfindingVisualizer:
    """Handles visualization of pathfinding algorithms."""

    def __init__(self):
        self.window = pygame.display.set_mode((constants.WIDTH + 250, constants.WIDTH))
        pygame.display.set_caption("Pathfinding Visualizer")
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 22, bold=True)

    def draw_grid(self, grid: List[List[Block]], algorithm_name: str = "A*",
                  next_action: str = "Place Start") -> None:
        """Draw blocks, grid lines, and side panel."""
        self.window.fill(constants.BLACK)

        for row in grid:
            for block in row:
                block.draw(self.window)

        self._draw_grid_lines()
        self._draw_side_panel(algorithm_name, next_action)
        pygame.display.update()

    def _draw_grid_lines(self) -> None:
        """Draw grid lines."""
        for i in range(constants.ROWS):
            pygame.draw.line(
                self.window,
                constants.GREY,
                (0, i * constants.GAP),
                (constants.WIDTH, i * constants.GAP)
            )
            pygame.draw.line(
                self.window,
                constants.GREY,
                (i * constants.GAP, 0),
                (i * constants.GAP, constants.WIDTH)
            )

    def _draw_side_panel(self, algorithm_name: str, next_action: str) -> None:
        """Draw side panel with controls and status."""
        panel_x = constants.WIDTH + 10

        # Status section
        title = self.title_font.render("STATUS", True, constants.WHITE)
        self.window.blit(title, (panel_x, 20))

        algo_text = self.font.render(f"Algorithm: {algorithm_name}", True, constants.GREEN)
        self.window.blit(algo_text, (panel_x, 60))

        action_text = self.font.render(f"Next: {next_action}", True, constants.YELLOW)
        self.window.blit(action_text, (panel_x, 90))

        # Controls section
        y = 150
        controls_title = self.title_font.render("CONTROLS", True, constants.WHITE)
        self.window.blit(controls_title, (panel_x, y))

        controls = [
            "Left Click:",
            "  Place blocks",
            "",
            "Right Click:",
            "  Erase blocks",
            "",
            "SPACE: Run",
            "C: Clear grid",
            "M: Generate maze",
            "",
            "1: A* algorithm",
            "2: Dijkstra",
            "",
            "ESC: Quit"
        ]

        for i, text in enumerate(controls):
            surface = self.font.render(text, True, constants.WHITE)
            self.window.blit(surface, (panel_x, y + 40 + i * 25))

    def animate_search(self, grid: List[List[Block]], visited: List[Block],
                       start: Block, end: Block, algorithm_name: str, delay_ms: int = 10) -> None:
        """Animate algorithm search process."""
        for block in visited:
            if block != start and block != end:
                block.set_closed()
                self.draw_grid(grid, algorithm_name, "Searching...")
                pygame.time.delay(delay_ms)

    def animate_path(self, grid: List[List[Block]], path: List[Block],
                     start: Block, end: Block, algorithm_name: str, delay_ms: int = 30) -> None:
        """Animate final path."""
        for block in path:
            if block != start and block != end:
                block.set_path()
                self.draw_grid(grid, algorithm_name, "Path Found!")
                pygame.time.delay(delay_ms)

        start.set_start()
        end.set_end()
        self.draw_grid(grid, algorithm_name, "Complete")

    def get_clicked_block(self, grid: List[List[Block]]) -> Optional[Block]:
        """Get block at mouse position."""
        pos = pygame.mouse.get_pos()
        row = pos[0] // constants.GAP
        col = pos[1] // constants.GAP

        if row < len(grid) and col < len(grid[0]) and pos[0] < constants.WIDTH:
            return grid[row][col]
        return None


def create_grid() -> List[List[Block]]:
    """Create empty grid of blocks."""
    grid = []
    for i in range(constants.ROWS):
        grid_row = []
        for j in range(constants.ROWS):
            block = Block(i, j, constants.GAP, constants.ROWS)
            grid_row.append(block)
        grid.append(grid_row)
    return grid