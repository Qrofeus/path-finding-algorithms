# Path-Finding Algorithms

Graphical simulations demonstrating the functionality of various path-finding algorithms using Python and Pygame.

Path-finding algorithms are essential in computing the shortest paths between points, with applications in navigation,
gaming, and network routing. This project visualizes these algorithms to enhance understanding of their operations and
differences.

## Implemented Algorithm(s)

- **A\* Algorithm**: Combines heuristics and cost functions to find the shortest path efficiently.

## Features

- **Interactive Visualization**: Observe each algorithm's decision-making process in real-time.

- **Customizable Grid**: Define start and end points, and set obstacles to simulate various scenarios.

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

- **Left Mouse Click**: Place the start, end, or obstacle blocks.

- **Right Mouse Click**: Reset start / end / obstacle blocks from the grid.

- **SPACE**: Start the path-finding algorithm.

- **c**: Clear the grid.

## File Structure

- `main.py`: Entry point for the application; handles user interaction and visualization.

- `algorithm/`: Contains implementations of the path-finding algorithms.

- `block.py`: Defines the `Block` class representing each cell in the grid.

- `ui.py`: Manages the graphical user interface components.

- `CONSTANTS.txt`: Stores configuration constants such as colors and grid dimensions.

- `read_file.py`: Handles reading configurations from `CONSTANTS.txt`.

- `requirements.txt`: Lists required Python packages.

## Acknowledgments

- This project was inspired by [Tech With Tim's A* Path-Finding Visualization](https://github.com/techwithtim/A-Path-Finding-Visualization). 