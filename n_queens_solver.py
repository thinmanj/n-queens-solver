"""N-Queens Problem Solver.

This module solves the classic N-Queens problem using a backtracking algorithm.
The goal is to place N queens on an N×N chessboard such that no two queens
threat each other (same row, column, or diagonal).
"""

import argparse
import sys
from typing import List, Optional


class NQueensSolver:
    """Solves the N-Queens problem using backtracking.
    
    Attributes:
        n: The size of the chessboard (N×N)
        board: 2D list representing the chessboard (1 = queen, 0 = empty)
        solutions_count: Number of solutions found
        verbose: Whether to print progress information
    """

    def __init__(self, n: int, verbose: bool = False):
        """Initialize the N-Queens solver.
        
        Args:
            n: Size of the chessboard
            verbose: Enable verbose output during solving
            
        Raises:
            ValueError: If n < 1
        """
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.board: List[List[int]] = [[0] * n for _ in range(n)]
        self.solutions_count = 0
        self.verbose = verbose

    def solve(self) -> bool:
        """Solve the N-Queens problem and display the result.
        
        Returns:
            True if a solution was found, False otherwise
        """
        if self.verbose:
            print(f"Solving {self.n}-Queens problem...")
        
        if self._backtrack(0):
            self._print_board()
            return True
        else:
            print(f"No solution exists for {self.n}-Queens problem.")
            return False

    def _backtrack(self, col: int) -> bool:
        """Recursively place queens using backtracking.
        
        Args:
            col: Current column to place a queen
            
        Returns:
            True if queens can be placed successfully, False otherwise
        """
        # Base case: all queens are placed
        if col >= self.n:
            return True

        # Try placing a queen in each row of the current column
        for row in range(self.n):
            if self._is_safe(row, col):
                # Place the queen
                self.board[row][col] = 1
                
                if self.verbose:
                    print(f"Placed queen at ({row}, {col})")

                # Recursively place the rest of the queens
                if self._backtrack(col + 1):
                    return True

                # Backtrack: remove the queen
                self.board[row][col] = 0
                if self.verbose:
                    print(f"Backtracked from ({row}, {col})")

        return False

    def _is_safe(self, row: int, col: int) -> bool:
        """Check if it's safe to place a queen at board[row][col].
        
        Args:
            row: Row position
            col: Column position
            
        Returns:
            True if position is safe, False otherwise
        """
        # Check row on the left side
        for j in range(col):
            if self.board[row][j] == 1:
                return False

        # Check upper diagonal on left side
        i, j = row, col
        while i >= 0 and j >= 0:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j -= 1

        # Check lower diagonal on left side
        i, j = row, col
        while i < self.n and j >= 0:
            if self.board[i][j] == 1:
                return False
            i += 1
            j -= 1

        return True

    def _print_board(self) -> None:
        """Print the chessboard with queens marked as 'Q'."""
        print("\n" + "=" * (4 * self.n + 1))
        for i in range(self.n):
            print("|", end="")
            for j in range(self.n):
                if self.board[i][j] == 1:
                    print(" Q ", end="|")
                else:
                    print("   ", end="|")
            print()
            print("=" * (4 * self.n + 1))
        print(f"\nSolution found for {self.n}-Queens problem!\n")

    def get_solution(self) -> Optional[List[int]]:
        """Get the solution as a list of row positions for each column.
        
        Returns:
            List of row indices where queens are placed, or None if not solved
        """
        solution = []
        for col in range(self.n):
            for row in range(self.n):
                if self.board[row][col] == 1:
                    solution.append(row)
                    break
        return solution if len(solution) == self.n else None


def main():
    """Main entry point for the N-Queens solver."""
    parser = argparse.ArgumentParser(
        description="Solve the N-Queens problem using backtracking.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python n_queens_solver.py 8          # Solve 8-Queens
  python n_queens_solver.py 20 -v     # Solve 20-Queens with verbose output
        """
    )
    parser.add_argument(
        "n",
        type=int,
        nargs="?",
        default=8,
        help="Size of the chessboard (default: 8)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if args.n < 1:
        print("Error: Board size must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.n in [2, 3]:
        print(f"Warning: No solution exists for {args.n}-Queens problem.")
    
    # Solve the problem
    try:
        solver = NQueensSolver(args.n, verbose=args.verbose)
        solver.solve()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
