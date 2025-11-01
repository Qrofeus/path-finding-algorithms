"""Tests for Block and BlockState classes."""

import pytest
from blocks.block import Block
from blocks import block_state


class TestBlockStates:
    """Test individual state behaviors."""

    def test_empty_state_properties(self):
        state = block_state.EMPTY
        assert state.is_walkable()
        assert state.get_color() == (255, 255, 255)

    def test_barrier_state_properties(self):
        state = block_state.BARRIER
        assert not state.is_walkable()
        assert state.get_color() == (0, 0, 0)

    def test_start_state_properties(self):
        state = block_state.START
        assert state.is_walkable()
        assert state.get_color() == (255, 165, 0)

    def test_end_state_properties(self):
        state = block_state.END
        assert state.is_walkable()
        assert state.get_color() == (128, 0, 128)

    def test_open_state_properties(self):
        state = block_state.OPEN
        assert state.is_walkable()
        assert state.get_color() == (0, 255, 0)

    def test_closed_state_properties(self):
        state = block_state.CLOSED
        assert state.is_walkable()
        assert state.get_color() == (255, 0, 0)

    def test_path_state_properties(self):
        state = block_state.PATH
        assert state.is_walkable()
        assert state.get_color() == (64, 224, 208)


class TestStateTransitions:
    """Test state transition validation."""

    def test_empty_to_any_transition(self):
        empty = block_state.EMPTY
        assert empty.can_transition_to(block_state.BARRIER)
        assert empty.can_transition_to(block_state.START)
        assert empty.can_transition_to(block_state.END)
        assert empty.can_transition_to(block_state.OPEN)

    def test_barrier_only_to_empty(self):
        barrier = block_state.BARRIER
        assert barrier.can_transition_to(block_state.EMPTY)
        assert barrier.can_transition_to(block_state.BARRIER)
        assert not barrier.can_transition_to(block_state.START)
        assert not barrier.can_transition_to(block_state.END)

    def test_start_cannot_become_end(self):
        start = block_state.START
        assert not start.can_transition_to(block_state.END)
        assert start.can_transition_to(block_state.EMPTY)
        assert start.can_transition_to(block_state.START)

    def test_end_cannot_become_start(self):
        end = block_state.END
        assert not end.can_transition_to(block_state.START)
        assert end.can_transition_to(block_state.EMPTY)
        assert end.can_transition_to(block_state.END)

    def test_algorithm_state_flow(self):
        open_state = block_state.OPEN
        assert open_state.can_transition_to(block_state.CLOSED)
        assert open_state.can_transition_to(block_state.PATH)

        closed_state = block_state.CLOSED
        assert closed_state.can_transition_to(block_state.PATH)
        assert closed_state.can_transition_to(block_state.EMPTY)


class TestBlockInitialization:
    """Test Block initialization."""

    def test_block_starts_empty(self):
        block = Block(row=5, col=10, width=16, total_rows=50)
        assert block.is_empty()
        assert block.get_position() == (5, 10)

    def test_block_coordinates(self):
        block = Block(row=3, col=4, width=20, total_rows=50)
        assert block.x == 60
        assert block.y == 80

    def test_reset_clears_state(self):
        block = Block(0, 0, 16, 50)
        block.set_barrier()
        block.reset()
        assert block.is_empty()


class TestBlockStateChanges:
    """Test Block state modification."""

    @pytest.fixture
    def block(self):
        return Block(row=0, col=0, width=16, total_rows=50)

    def test_set_and_check_barrier(self, block):
        block.set_barrier()
        assert block.is_barrier()
        assert not block.is_walkable()

    def test_set_and_check_start(self, block):
        block.set_start()
        assert block.is_start()
        assert block.is_walkable()

    def test_set_and_check_end(self, block):
        block.set_end()
        assert block.is_end()
        assert block.is_walkable()

    def test_algorithm_states(self, block):
        block.set_open()
        assert block.is_open()

        block.set_closed()
        assert block.is_closed()
        assert not block.is_open()

        block.set_path()
        assert not block.is_closed()


class TestInvalidTransitions:
    """Test that invalid transitions are rejected."""

    def test_barrier_to_start_rejected(self):
        block = Block(0, 0, 16, 50)
        block.set_barrier()

        success = block.set_state(block_state.START)
        assert not success
        assert block.is_barrier()

    def test_start_to_end_rejected(self):
        block = Block(0, 0, 16, 50)
        block.set_start()

        success = block.set_state(block_state.END)
        assert not success
        assert block.is_start()

    def test_valid_transition_succeeds(self):
        block = Block(0, 0, 16, 50)
        block.set_barrier()

        success = block.set_state(block_state.EMPTY)
        assert success
        assert block.is_empty()


class TestNeighborCalculation:
    """Test neighbor finding logic."""

    def create_grid(self, rows=3):
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(rows):
                block = Block(row, col, width=16, total_rows=rows)
                grid_row.append(block)
            grid.append(grid_row)
        return grid

    def test_center_has_four_neighbors(self):
        grid = self.create_grid(3)
        center = grid[1][1]
        center.update_neighbors(grid)
        assert len(center.neighbors) == 4

    def test_corner_has_two_neighbors(self):
        grid = self.create_grid(3)
        corner = grid[0][0]
        corner.update_neighbors(grid)
        assert len(corner.neighbors) == 2

    def test_edge_has_three_neighbors(self):
        grid = self.create_grid(3)
        edge = grid[0][1]
        edge.update_neighbors(grid)
        assert len(edge.neighbors) == 3

    def test_barrier_excluded_from_neighbors(self):
        grid = self.create_grid(3)
        center = grid[1][1]
        grid[1][0].set_barrier()

        center.update_neighbors(grid)
        assert len(center.neighbors) == 3
        assert grid[1][0] not in center.neighbors

    def test_is_neighbor_check(self):
        grid = self.create_grid(3)
        block1 = grid[0][0]
        block2 = grid[0][1]
        block3 = grid[2][2]

        block1.update_neighbors(grid)
        assert block1.is_neighbor(block2)
        assert not block1.is_neighbor(block3)


class TestEdgeCases:
    """Test boundary conditions."""

    def test_single_block_no_neighbors(self):
        grid = [[Block(0, 0, 16, 1)]]
        block = grid[0][0]
        block.update_neighbors(grid)
        assert len(block.neighbors) == 0

    def test_all_barriers_no_walkable_neighbors(self):
        grid = []
        for i in range(3):
            row = []
            for j in range(3):
                block = Block(i, j, 16, 3)
                block.set_barrier()
                row.append(block)
            grid.append(row)

        center = grid[1][1]
        center.update_neighbors(grid)
        assert len(center.neighbors) == 0

    def test_block_string_representation(self):
        block = Block(5, 10, 16, 50)
        block.set_barrier()
        repr_str = repr(block)
        assert "Block(5, 10" in repr_str
        assert "BarrierState" in repr_str

# # All tests
# pytest tests/test_block.py -v
#
# # With coverage
# pytest tests/test_block.py --cov=blocks --cov-report=html
#
# # Specific test class
# pytest tests/test_block.py::TestStateTransitions -v