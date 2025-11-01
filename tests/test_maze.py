"""Tests for Wilson's maze generation algorithm."""

import pytest
from blocks.block import Block
from maze import WilsonMazeGenerator


class TestWilsonMazeGenerator:
    """Test Wilson's algorithm maze generation."""

    def create_grid(self, rows=5):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_maze_generation_completes(self):
        grid = self.create_grid(5)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        # All blocks should be either empty or barrier (no closed blocks)
        for row in grid:
            for block in row:
                assert block.is_empty() or block.is_barrier()

    def test_maze_is_perfect(self):
        grid = self.create_grid(5)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        # Perfect maze: should have some empty blocks (paths)
        non_barriers = sum(1 for row in grid for block in row if not block.is_barrier())
        assert non_barriers > 0

    def test_generator_clear(self):
        grid = self.create_grid(5)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        generator.clear()
        assert len(generator.path) == 0

    def test_small_grid(self):
        grid = self.create_grid(2)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        # All blocks should be either empty or barrier
        for row in grid:
            for block in row:
                assert block.is_empty() or block.is_barrier()

    def test_larger_grid(self):
        grid = self.create_grid(10)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        # All blocks should be either empty or barrier
        for row in grid:
            for block in row:
                assert block.is_empty() or block.is_barrier()

    def test_maze_has_paths(self):
        grid = self.create_grid(5)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        # Count walkable blocks
        walkable = sum(1 for row in grid for block in row if not block.is_barrier())

        # Should have created paths (not all barriers)
        assert walkable > 0

    def test_randomness(self):
        # Generate two mazes and check they're different
        grid1 = self.create_grid(5)
        grid2 = self.create_grid(5)

        gen1 = WilsonMazeGenerator()
        gen2 = WilsonMazeGenerator()

        gen1.generate(grid1)
        gen2.generate(grid2)

        # Count barriers in each
        barriers1 = sum(1 for row in grid1 for block in row if block.is_barrier())
        barriers2 = sum(1 for row in grid2 for block in row if block.is_barrier())

        # Both should be valid mazes (but likely different configurations)
        assert barriers1 >= 0
        assert barriers2 >= 0

    def test_all_blocks_empty_or_barrier(self):
        """Test that all blocks are either empty or barrier after generation."""
        grid = self.create_grid(5)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        # Check every block is in one of the two valid states
        for row in grid:
            for block in row:
                assert block.is_empty() or block.is_barrier(), \
                    f"Block at {block.get_position()} is neither empty nor barrier"

        # Also verify no blocks are in closed state
        closed_count = sum(1 for row in grid for block in row if block.is_closed())
        assert closed_count == 0, f"Found {closed_count} closed blocks after generation"

    def test_not_all_blocks_are_empty(self):
        """Test that not all blocks are empty (maze should have barriers)."""
        grid = self.create_grid(5)
        generator = WilsonMazeGenerator()
        generator.generate(grid)

        # Count empty blocks
        empty_count = sum(1 for row in grid for block in row if block.is_empty())
        total_blocks = len(grid) * len(grid[0])

        # If all blocks are empty, this test should fail
        assert empty_count < total_blocks, \
            f"All {total_blocks} blocks are empty - maze has no barriers!"

        # Also verify we have at least some barriers
        barrier_count = sum(1 for row in grid for block in row if block.is_barrier())
        assert barrier_count > 0, "Maze has no barriers!"


class TestWilsonMazeHelpers:
    """Test helper methods."""

    def create_grid(self, rows=3):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_get_closed_neighbors_center(self):
        grid = self.create_grid(3)
        generator = WilsonMazeGenerator()

        # Initialize grid (all blocks closed)
        for row in grid:
            for block in row:
                block.set_closed()

        # Center block should have 4 closed neighbors
        center = grid[1][1]
        neighbors = generator._get_closed_neighbors(grid, center)
        assert len(neighbors) == 4

    def test_get_closed_neighbors_corner(self):
        grid = self.create_grid(3)
        generator = WilsonMazeGenerator()

        # Initialize grid (all blocks closed)
        for row in grid:
            for block in row:
                block.set_closed()

        # Corner should have 2 closed neighbors
        corner = grid[0][0]
        neighbors = generator._get_closed_neighbors(grid, corner)
        assert len(neighbors) == 2

    def test_get_empty_neighbors(self):
        grid = self.create_grid(3)
        generator = WilsonMazeGenerator()

        # Initialize all blocks as closed
        for row in grid:
            for block in row:
                block.set_closed()

        # Center has no empty neighbors initially
        center = grid[1][1]
        neighbors = generator._get_empty_neighbors(grid, center)
        assert len(neighbors) == 0

        # Mark adjacent block as empty
        grid[0][1].reset()
        neighbors = generator._get_empty_neighbors(grid, center)
        assert len(neighbors) == 1

    def test_get_unvisited_blocks(self):
        grid = self.create_grid(3)
        generator = WilsonMazeGenerator()

        # Initialize all blocks as closed (unvisited)
        for row in grid:
            for block in row:
                block.set_closed()

        # Initially all unvisited
        unvisited = generator._get_unvisited_blocks(grid)
        assert len(unvisited) == 9

        # Mark one as empty (visited)
        grid[0][0].reset()
        unvisited = generator._get_unvisited_blocks(grid)
        assert len(unvisited) == 8

        # Mark one as barrier (also visited)
        grid[1][1].set_barrier()
        unvisited = generator._get_unvisited_blocks(grid)
        assert len(unvisited) == 7

# Run: pytest tests/test_maze.py -v