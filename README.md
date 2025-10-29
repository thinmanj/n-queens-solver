# N-Queens Solver

A Python implementation of the classic N-Queens problem using backtracking algorithm with constraint propagation optimization.

## Overview

The N-Queens problem is a classic combinatorial puzzle that asks: "How can N chess queens be placed on an N×N chessboard so that no two queens threaten each other?" This means no two queens can share the same row, column, or diagonal.

This implementation uses a backtracking algorithm enhanced with constraint propagation to efficiently solve the problem for various board sizes.

## Features

- ✅ Solves N-Queens problem for any board size
- ✅ Clean, efficient backtracking algorithm
- ✅ Command-line interface with argument parsing
- ✅ Visual board output with formatted table
- ✅ Optional verbose mode for debugging
- ✅ Type hints for better code quality
- ✅ Comprehensive docstrings
- ✅ Graceful error handling

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/n-queens-solver.git
cd n-queens-solver
```

No external dependencies required - uses only Python standard library.

## Usage

### Basic Usage

Run the solver with default settings (8-Queens):

```bash
python n_queens_solver.py
```

### Specify Board Size

Solve for any N-Queens problem:

```bash
python n_queens_solver.py 4    # Solve 4-Queens
python n_queens_solver.py 12   # Solve 12-Queens
python n_queens_solver.py 100  # Solve 100-Queens
```

### Verbose Mode

See step-by-step progress:

```bash
python n_queens_solver.py 8 -v
python n_queens_solver.py 8 --verbose
```

### Help

View all available options:

```bash
python n_queens_solver.py --help
```

### Example Output

For an 8×8 board:

```
=================================
| Q |   |   |   |   |   |   |   |
=================================
|   |   |   |   |   |   | Q |   |
=================================
|   |   |   |   | Q |   |   |   |
=================================
|   |   |   |   |   |   |   | Q |
=================================
|   | Q |   |   |   |   |   |   |
=================================
|   |   |   | Q |   |   |   |   |
=================================
|   |   |   |   |   | Q |   |   |
=================================
|   |   | Q |   |   |   |   |   |
=================================

Solution found for 8-Queens problem!
```

## Algorithm

The solver uses a classic **backtracking** algorithm:

1. **Column-by-Column Placement**: Places queens one column at a time, from left to right
2. **Safety Check**: For each column, tries each row and checks if placing a queen there is safe:
   - No other queen in the same row
   - No other queen in the upper-left diagonal
   - No other queen in the lower-left diagonal
3. **Recursion**: If placement is safe, recursively attempts to place remaining queens
4. **Backtracking**: If no safe position exists, backtracks to the previous column and tries a different row

### Key Components

- `NQueensSolver`: Main solver class
- `solve()`: Entry point that initiates the solving process
- `_backtrack(col)`: Recursive backtracking function that places queens
- `_is_safe(row, col)`: Validates if a queen can be safely placed at a position
- `_print_board()`: Displays the final solution with formatted output
- `get_solution()`: Returns the solution as a list of row positions

### Time Complexity

- **Worst case**: O(N!) - backtracking explores all permutations
- **Average case**: Significantly better due to constraint propagation pruning

## Examples

### Small Board (4-Queens)

```bash
$ python n_queens_solver.py 4

=================
|   |   | Q |   |
=================
| Q |   |   |   |
=================
|   |   |   | Q |
=================
|   | Q |   |   |
=================

Solution found for 4-Queens problem!
```

### Standard Chess Board (8-Queens)

```bash
$ python n_queens_solver.py 8
# Outputs an 8x8 board with queens placed
```

### Large Board with Verbose Mode

```bash
$ python n_queens_solver.py 12 -v
Solving 12-Queens problem...
Placed queen at (0, 0)
Placed queen at (2, 1)
# ... shows all placements and backtracks
```

### Using as a Module

```python path=null start=null
from n_queens_solver import NQueensSolver

# Create solver instance
solver = NQueensSolver(n=8, verbose=False)

# Solve the problem
if solver.solve():
    # Get solution as list of row positions
    solution = solver.get_solution()
    print(f"Solution: {solution}")
```

## Limitations

- Only finds **one valid solution** (not all solutions)
- Some board sizes have no solution (e.g., N=2, N=3)
- Memory usage increases with O(N²) for the board representation

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest enhancements
- Submit pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

The N-Queens problem has been studied since the 19th century and remains a popular example for teaching backtracking algorithms and constraint satisfaction problems.

## References

- [N-Queens Problem on Wikipedia](https://en.wikipedia.org/wiki/Eight_queens_puzzle)
- Backtracking Algorithm
- Constraint Satisfaction Problems
