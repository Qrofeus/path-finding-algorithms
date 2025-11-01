# AlgoViz: Interactive Pathfinding & Maze Generation

Graphical simulations demonstrating the functionality of various path-finding algorithms using Python and Pygame.

Path-finding algorithms are essential in computing the shortest paths between points, with applications in navigation,
gaming, and network routing. This project visualizes these algorithms to enhance understanding of their operations and
differences.

## Implemented Algorithms

- **A\* Algorithm**: Combines heuristics (Manhattan distance) and cost functions to find the shortest path efficiently. Uses f(n) = g(n) + h(n) for optimal pathfinding.

- **Dijkstra's Algorithm**: Uniform cost search without heuristics. Explores all directions equally, guaranteeing the shortest path.

## Features

- **Multiple Algorithms**: Switch between A\* and Dijkstra's algorithm with keyboard shortcuts.

- **Interactive Visualization**: Observe each algorithm's decision-making process in real-time with animated search and path reconstruction.

- **Customizable Grid**: Define start and end points, and set obstacles to simulate various scenarios.

- **Maze Generation**: Generate random mazes using Wilson's algorithm (unbiased maze generation).

- **Drag-to-Draw**: Click and drag to place or erase barriers for quick grid setup.

## Usage

1. Clone the repository:
```bash
git clone https://github.com/Qrofeus/path-finding-algorithms
```
2. Navigate to the project directory:
```bash
cd path-finding-algorithms
```
3. Run the main script:
```bash
python main.py
```

## Requirements

- Python 3.x

- Pygame

Install the required packages using:

```bash
pip install -r requirements.txt
```

## How to Use

### Mouse Controls
- **Left Mouse Click**: Place the start point (first click), end point (second click), or barriers (subsequent clicks).
- **Left Mouse Drag**: Continuously place barriers while holding the button.
- **Right Mouse Click/Drag**: Erase start, end, or barrier blocks.

### Keyboard Controls
- **SPACE**: Run the currently selected pathfinding algorithm.
- **1**: Switch to A\* algorithm.
- **2**: Switch to Dijkstra's algorithm.
- **M**: Generate a random maze using Wilson's algorithm.
- **C**: Clear the entire grid.
- **ESC**: Quit the application.

## Project Structure

```
path-finding-algorithms/
├── main.py                    # Application entry point and event loop
├── visualizer.py              # UI rendering and animation
├── algorithms/                # Pathfinding algorithm implementations
│   ├── __init__.py
│   ├── base_pathfinder.py    # Abstract base class (Strategy Pattern)
│   ├── a_star.py             # A* algorithm implementation
│   └── dijkstra.py           # Dijkstra's algorithm implementation
├── blocks/                    # Grid cell representations
│   ├── __init__.py
│   ├── block.py              # Block class with position and neighbors
│   └── block_state.py        # State Pattern for block behaviors
├── maze/                      # Maze generation algorithms
│   ├── __init__.py
│   └── wilson_maze.py        # Wilson's algorithm for maze generation
├── config/                    # Configuration and constants
│   ├── __init__.py
│   └── constants.py          # Display settings and color definitions
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_algorithms.py    # Algorithm tests
│   ├── test_block.py         # Block and state tests
│   ├── test_integration.py   # Integration tests
│   └── test_maze.py          # Maze generation tests
└── requirements.txt           # Python dependencies
```

## Design Patterns

This project implements several design patterns to ensure clean, maintainable, and extensible code:

### Strategy Pattern
- **Location**: `algorithms/base_pathfinder.py`
- **Purpose**: Allows switching between different pathfinding algorithms (A\*, Dijkstra) at runtime.
- **Implementation**: `BasePathfinder` is an abstract base class that defines the interface. Each algorithm (A\*, Dijkstra) implements the `find_path()` method with its own strategy.
- **Benefit**: Easy to add new algorithms without modifying existing code.

### State Pattern
- **Location**: `blocks/block_state.py`
- **Purpose**: Manages block behavior based on its current state (Empty, Barrier, Start, End, Open, Closed, Path).
- **Implementation**: Each state is a class that defines its own color, walkability, and valid transitions.
- **Benefit**: Encapsulates state-specific behavior and prevents invalid state transitions.

## Running Tests

This project includes a comprehensive test suite using pytest.

### Install Test Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage Report
```bash
pytest --cov=algorithms --cov=blocks --cov=maze
```

### Run Specific Test Files
```bash
# Test pathfinding algorithms
pytest tests/test_algorithms.py

# Test block functionality
pytest tests/test_block.py

# Test maze generation
pytest tests/test_maze.py

# Run integration tests
pytest tests/test_integration.py
```

### Run Tests in Verbose Mode
```bash
pytest -v
```

## Acknowledgments

- This project was inspired by [Tech With Tim's A* Path-Finding Visualization](https://github.com/techwithtim/A-Path-Finding-Visualization). 