# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python implementation of the N-Queens problem solver using an optimized backtracking algorithm with constraint propagation. The entire implementation is contained in a single module: `n_queens_solver.py`.

The project uses only Python's standard library - no external dependencies.

## Commands

### Run the solver
```bash
python n_queens_solver.py [N] [-v|--verbose]
```
- Default N=8 if not specified
- Use `-v` or `--verbose` for detailed execution output
- Examples:
  - `python n_queens_solver.py` - Solve standard 8-Queens
  - `python n_queens_solver.py 12` - Solve 12-Queens
  - `python n_queens_solver.py 20 -v` - Solve with verbose output

### Help
```bash
python n_queens_solver.py --help
```

### Testing
No formal test framework is configured. To test changes:
1. Run with known solvable sizes: 4, 8, 12, 20
2. Verify known unsolvable sizes fail gracefully: 2, 3
3. Use verbose mode to debug algorithm behavior

## Architecture

### Core Algorithm
The solver uses **backtracking with O(1) constraint checking** via set-based tracking:

- **NQueensSolver class**: Main solver implementing the backtracking algorithm
- **1D board representation**: `board[col] = row` - stores which row has a queen in each column
- **Constraint tracking**: Three sets for O(1) conflict detection:
  - `cols`: Occupied rows
  - `diag1`: Occupied positive diagonals (row - col)
  - `diag2`: Occupied negative diagonals (row + col)

### Key Methods
- `solve()`: Entry point that calls backtracking and displays results
- `_backtrack(col)`: Recursive core algorithm placing queens column by column
- `_is_safe()`: NOT USED - constraint checking is done via set membership (O(1))
- `_print_board()`: Visual output formatting
- `get_solution()`: Returns solution as list of row positions

### Algorithm Flow
1. Place queens column by column (left to right)
2. For each column, try each row
3. Check conflicts in O(1) using set membership tests
4. Recursively solve remaining columns
5. Backtrack if no valid placement exists

### Important Implementation Details
- The algorithm finds **only one solution**, not all solutions
- Board sizes N=2 and N=3 have no solutions
- Time complexity: O(N!) worst case, but pruning significantly improves average case
- Space complexity: O(N) for constraint tracking

## Module Usage

The solver can be imported and used programmatically:

```python
from n_queens_solver import NQueensSolver

solver = NQueensSolver(n=8, verbose=False)
if solver.solve():
    solution = solver.get_solution()  # Returns list of row positions
```

## Code Style Notes

- Uses type hints throughout
- Comprehensive docstrings with Args/Returns/Raises sections
- Set-based optimization preferred over array scanning
- Error handling for edge cases (n < 1, KeyboardInterrupt)
