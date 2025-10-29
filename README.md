# N-Queens Solver

A Python implementation of the classic N-Queens problem using backtracking algorithm with constraint propagation optimization.

## Overview

The N-Queens problem is a classic combinatorial puzzle that asks: "How can N chess queens be placed on an N×N chessboard so that no two queens threaten each other?" This means no two queens can share the same row, column, or diagonal.

This implementation uses a backtracking algorithm enhanced with constraint propagation to efficiently solve the problem for various board sizes.

## Features

- ✅ Solves N-Queens problem for any board size
- ✅ Backtracking algorithm with optimization
- ✅ Constraint propagation to reduce search space
- ✅ Visual board output showing queen positions
- ✅ Progress tracking during computation

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/n-queens-solver.git
cd n-queens-solver
```

No external dependencies required - uses only Python standard library.

## Usage

Run the solver directly:

```bash
python n_queens_solver.py
```

By default, the program solves the 100-Queens problem. To solve for a different board size, modify the initialization in the `__main__` block:

```python path=null start=null
if __name__ == '__main__':
    queens = QueensProblem(8)  # Change to desired board size
    queens.solve_n_queens()
```

### Example Output

For an 8×8 board:

```
 Q  0  0  0  0  0  0  0 

 0  0  0  0  Q  0  0  0 

 0  0  0  0  0  0  0  Q 

 0  0  0  0  0  Q  0  0 

 0  0  Q  0  0  0  0  0 

 0  0  0  0  0  0  Q  0 

 0  Q  0  0  0  0  0  0 

 0  0  0  Q  0  0  0  0 
```

## Algorithm

The solver uses **backtracking** combined with **constraint propagation**:

1. **Backtracking**: Places queens column by column, trying different rows in each column
2. **Constraint Propagation**: Marks cells that become invalid when a queen is placed, reducing the search space
3. **Validation**: Before placing a queen, ensures no future columns would be completely blocked

### Key Components

- `solve_n_queens()`: Entry point that initiates the solving process
- `solve(col_index)`: Recursive backtracking function
- `is_place_valid(row, col)`: Validates if a queen can be placed at a position
- `mark_position(row, col)`: Updates constraint markers when placing/removing queens
- `print_queens()`: Displays the final solution

### Time Complexity

- **Worst case**: O(N!) - backtracking explores all permutations
- **Average case**: Significantly better due to constraint propagation pruning

## Examples

### Small Board (4-Queens)

```python path=null start=null
queens = QueensProblem(4)
queens.solve_n_queens()
```

### Standard Chess Board (8-Queens)

```python path=null start=null
queens = QueensProblem(8)
queens.solve_n_queens()
```

### Large Board (100-Queens)

```python path=null start=null
queens = QueensProblem(100)
queens.solve_n_queens()
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
