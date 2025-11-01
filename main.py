"""
Main application entry point.

Handles event loop and coordinates between UI, algorithms, and maze generation.
"""

import pygame
from visualizer import PathfindingVisualizer, create_grid
from algorithms import AStarPathfinder, DijkstraPathfinder
from maze import WilsonMazeGenerator


class PathfindingApp:
    """Main application controller."""

    def __init__(self):
        pygame.init()
        self.visualizer = PathfindingVisualizer()
        self.grid = create_grid()

        self.start_block = None
        self.end_block = None

        self.algorithms = {
            'astar': ('A*', AStarPathfinder()),
            'dijkstra': ('Dijkstra', DijkstraPathfinder())
        }
        self.current_algorithm = 'astar'

        self.maze_generator = WilsonMazeGenerator()
        self.running = True

        self.is_dragging = False
        self.drag_mode = None

    def get_algorithm_name(self) -> str:
        """Get display name of current algorithm."""
        return self.algorithms[self.current_algorithm][0]

    def get_next_action(self) -> str:
        """Get description of what next click will do."""
        if not self.start_block:
            return "Place Start"
        elif not self.end_block:
            return "Place End"
        else:
            return "Place Barriers"

    def run(self) -> None:
        """Main event loop."""
        while self.running:
            self.visualizer.draw_grid(self.grid, self.get_algorithm_name(), self.get_next_action())
            self._handle_events()

        pygame.quit()

    def _handle_events(self) -> None:
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event.button)

            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_drag()

            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)

    def _handle_mouse_down(self, button: int) -> None:
        """Handle mouse button press."""
        block = self.visualizer.get_clicked_block(self.grid)
        if not block:
            return

        if button == 1:  # Left click
            if not self.start_block and block != self.end_block:
                block.set_start()
                self.start_block = block

            elif not self.end_block and block != self.start_block:
                block.set_end()
                self.end_block = block

            elif block != self.start_block and block != self.end_block:
                block.set_barrier()
                self.is_dragging = True
                self.drag_mode = 'barrier'

        elif button == 3:  # Right click
            if block == self.start_block:
                self.start_block = None
            if block == self.end_block:
                self.end_block = None
            block.reset()
            self.is_dragging = True
            self.drag_mode = 'erase'

    def _handle_mouse_up(self, button: int) -> None:
        """Handle mouse button release."""
        self.is_dragging = False
        self.drag_mode = None

    def _handle_mouse_drag(self) -> None:
        """Handle mouse drag for continuous barrier placement."""
        if not self.is_dragging:
            return

        block = self.visualizer.get_clicked_block(self.grid)
        if not block:
            return

        if self.drag_mode == 'barrier':
            if block != self.start_block and block != self.end_block:
                block.set_barrier()

        elif self.drag_mode == 'erase':
            if block == self.start_block:
                self.start_block = None
            if block == self.end_block:
                self.end_block = None
            block.reset()

    def _handle_keypress(self, key: int) -> None:
        """Handle keyboard inputs."""
        if key == pygame.K_SPACE:
            self._run_algorithm()

        elif key == pygame.K_c:
            self._clear_grid()

        elif key == pygame.K_m:
            self._generate_maze()

        elif key == pygame.K_1:
            self.current_algorithm = 'astar'

        elif key == pygame.K_2:
            self.current_algorithm = 'dijkstra'

        elif key == pygame.K_ESCAPE:
            self.running = False

    def _run_algorithm(self) -> None:
        """Execute selected pathfinding algorithm."""
        if not self.start_block or not self.end_block:
            return

        for row in self.grid:
            for block in row:
                block.update_neighbors(self.grid)

        _, algorithm = self.algorithms[self.current_algorithm]
        result = algorithm.find_path(self.grid, self.start_block, self.end_block)

        self.visualizer.animate_search(self.grid, result.visited, self.start_block,
                                       self.end_block, self.get_algorithm_name())

        if result.found:
            self.visualizer.animate_path(self.grid, result.path, self.start_block,
                                         self.end_block, self.get_algorithm_name())

    def _clear_grid(self) -> None:
        """Reset grid to empty state."""
        self.start_block = None
        self.end_block = None
        self.grid = create_grid()

    def _generate_maze(self) -> None:
        """Generate maze using Wilson's algorithm."""
        self.start_block = None
        self.end_block = None
        self.grid = create_grid()
        self.maze_generator.clear()
        self.maze_generator.generate(self.grid)


def main():
    """Application entry point."""
    app = PathfindingApp()
    app.run()


if __name__ == '__main__':
    main()