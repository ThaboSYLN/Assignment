# Coin Sorting Solver

This project implements various search algorithms to solve the Coin Sorting Puzzle. The goal is to move coins across different positions while following specific rules.

## Features
- Implements **Depth-First Search (DFS), Breadth-First Search (BFS), Greedy Best-First Search, and A* Search**.
- Enforces movement constraints based on coin parity (odd/even).
- Provides a step-by-step solution for sorting coins efficiently.

## Requirements
- Python 3.x

## Usage
1. Run the script:
   ```sh
   python coin_sorting_solver.py
   ```
2. Enter the number of coins (4, 6, 8, or 10).
3. Choose a search algorithm to solve the puzzle.
4. View the step-by-step moves to solve the problem.

## Example Output
```
Enter number of coins: 4
Choose an algorithm:
1. Depth-first search
2. Breadth-first search
3. Greedy best-first search
4. A* search

Solving with A* search...
Solution found in X moves:
Move 1: A -> B
Move 2: E -> C
...
```

## License
MIT License
