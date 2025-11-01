"""Integration tests for complete pathfinding workflows."""

import pytest
from blocks.block import Block
from algorithms import AStarPathfinder, DijkstraPathfinder


class TestEndToEndPathfinding:
    """Test complete pathfinding workflows."""

    def create_grid(self, rows=10):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_astar_finds_path_in_open_grid(self):
        grid = self.create_grid(10)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[9][9]
        start.set_start()
        end.set_end()

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        assert start.is_start()
        assert end.is_end()
        assert result.get_path_length() == 18  # Manhattan distance

    def test_dijkstra_finds_path_in_open_grid(self):
        grid = self.create_grid(10)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[9][9]

        pathfinder = DijkstraPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        assert result.get_path_length() == 18

    def test_pathfinding_with_barriers(self):
        grid = self.create_grid(10)

        # Create barrier wall
        for i in range(8):
            grid[i][5].set_barrier()

        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[0][9]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        # Must go around barrier
        for block in result.path:
            assert not block.is_barrier()


class TestStateTransitionsDuringPathfinding:
    """Test block state changes during algorithm execution."""

    def create_grid(self, rows=5):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_blocks_marked_during_search(self):
        grid = self.create_grid(5)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[4][4]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        # Simulate visualization: mark visited blocks
        for block in result.visited:
            if block != start and block != end:
                block.set_closed()

        # Mark path
        for block in result.path:
            if block != start and block != end:
                block.set_path()

        # Verify closed blocks exist
        closed_count = sum(1 for row in grid for block in row if block.is_closed())
        assert closed_count > 0


class TestAlgorithmComparison:
    """Compare algorithm behavior on same scenarios."""

    def create_grid(self, rows=15):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_astar_vs_dijkstra_performance(self):
        grid = self.create_grid(15)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[14][14]

        astar = AStarPathfinder()
        dijkstra = DijkstraPathfinder()

        astar_result = astar.find_path(grid, start, end)
        dijkstra_result = dijkstra.find_path(grid, start, end)

        # Both find optimal path
        assert astar_result.get_path_length() == dijkstra_result.get_path_length()

        # A* visits fewer nodes due to heuristic
        assert len(astar_result.visited) <= len(dijkstra_result.visited)

# Run: pytest tests/test_integration.py -v