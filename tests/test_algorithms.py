"""Tests for pathfinding algorithms."""

import pytest
from blocks.block import Block
from algorithms import AStarPathfinder, DijkstraPathfinder, BasePathfinder
from algorithms.base_pathfinder import PathfindingResult


class TestPathfindingResult:
    """Test PathfindingResult container."""

    def test_successful_result(self):
        path = [Block(0, 0, 16, 10), Block(0, 1, 16, 10)]
        result = PathfindingResult(path, {}, [])
        assert result.found
        assert result.get_path_length() == 2

    def test_failed_result(self):
        result = PathfindingResult(None, {}, [])
        assert not result.found
        assert result.get_path_length() == 0


class TestBasePathfinder:
    """Test base pathfinder utilities."""

    def test_manhattan_distance(self):
        pathfinder = AStarPathfinder()
        distance = pathfinder.manhattan_distance((0, 0), (3, 4))
        assert distance == 7

    def test_reconstruct_path(self):
        pathfinder = AStarPathfinder()
        b1 = Block(0, 0, 16, 10)
        b2 = Block(0, 1, 16, 10)
        b3 = Block(0, 2, 16, 10)

        came_from = {b2: b1, b3: b2}
        path = pathfinder.reconstruct_path(came_from, b3)

        assert path == [b2, b3]


class TestGridSetup:
    """Shared test grid creation."""

    @staticmethod
    def create_grid(rows=5):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid)
        return grid

    @staticmethod
    def update_all_neighbors(grid):
        for row in grid:
            for block in row:
                block.update_neighbors(grid)


class TestAStarPathfinder:
    """Test A* algorithm."""

    def create_grid(self, rows=5):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_straight_line_path(self):
        grid = self.create_grid(5)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[0][4]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        assert result.get_path_length() == 4

    def test_path_with_barrier(self):
        grid = self.create_grid(5)

        # Create vertical barrier
        for i in range(4):
            grid[i][2].set_barrier()

        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[0][4]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        assert result.get_path_length() > 4  # Must go around

    def test_no_path_available(self):
        grid = self.create_grid(5)

        # Create complete barrier
        for i in range(5):
            grid[i][2].set_barrier()

        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[0][4]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert not result.found
        assert result.path is None

    def test_start_equals_end(self):
        grid = self.create_grid(5)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[2][2]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, start)

        assert result.found
        assert result.get_path_length() == 0

    def test_visited_blocks_tracked(self):
        grid = self.create_grid(5)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[4][4]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        assert len(result.visited) > 0


class TestDijkstraPathfinder:
    """Test Dijkstra's algorithm."""

    def create_grid(self, rows=5):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_straight_line_path(self):
        grid = self.create_grid(5)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[0][4]

        pathfinder = DijkstraPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        assert result.get_path_length() == 4

    def test_path_with_barrier(self):
        grid = self.create_grid(5)

        for i in range(4):
            grid[i][2].set_barrier()

        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[0][4]

        pathfinder = DijkstraPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found
        assert result.get_path_length() > 4

    def test_no_path_available(self):
        grid = self.create_grid(5)

        for i in range(5):
            grid[i][2].set_barrier()

        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[0][4]

        pathfinder = DijkstraPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert not result.found


class TestAlgorithmComparison:
    """Compare A* and Dijkstra behavior."""

    def create_grid(self, rows=10):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_both_find_same_path_length(self):
        grid = self.create_grid(10)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[9][9]

        astar = AStarPathfinder()
        dijkstra = DijkstraPathfinder()

        astar_result = astar.find_path(grid, start, end)
        dijkstra_result = dijkstra.find_path(grid, start, end)

        assert astar_result.found
        assert dijkstra_result.found
        assert astar_result.get_path_length() == dijkstra_result.get_path_length()

    def test_astar_visits_fewer_nodes(self):
        grid = self.create_grid(10)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[9][9]

        astar = AStarPathfinder()
        dijkstra = DijkstraPathfinder()

        astar_result = astar.find_path(grid, start, end)
        dijkstra_result = dijkstra.find_path(grid, start, end)

        # A* should visit fewer nodes due to heuristic
        assert len(astar_result.visited) <= len(dijkstra_result.visited)


class TestComplexScenarios:
    """Test complex pathfinding scenarios."""

    def create_grid(self, rows=10):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_maze_with_single_solution(self):
        grid = self.create_grid(5)

        # Create L-shaped path
        grid[1][0].set_barrier()
        grid[1][1].set_barrier()
        grid[1][2].set_barrier()
        grid[2][2].set_barrier()
        grid[3][2].set_barrier()

        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[4][4]

        pathfinder = AStarPathfinder()
        result = pathfinder.find_path(grid, start, end)

        assert result.found

    def test_path_quality_consistent(self):
        grid = self.create_grid(5)
        for row in grid:
            for block in row:
                block.update_neighbors(grid)

        start = grid[0][0]
        end = grid[4][4]

        pathfinder = AStarPathfinder()

        # Run multiple times - should get same result
        result1 = pathfinder.find_path(grid, start, end)
        result2 = pathfinder.find_path(grid, start, end)

        assert result1.get_path_length() == result2.get_path_length()

# # All algorithm tests
# pytest tests/test_algorithms.py -v
#
# # Specific test class
# pytest tests/test_algorithms.py::TestAlgorithmComparison -v
#
# # All tests
# pytest tests/ -v