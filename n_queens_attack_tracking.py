"""N-Queens Solver with Attack Cell Tracking.

This version maintains a 2D board tracking which cells are under attack,
based on the original approach but optimized.
"""

import argparse
import sys
from typing import List, Optional


class NQueensSolverWithTracking:
    """Solves N-Queens by tracking attacked cells on a 2D board.
    
    Each cell stores how many queens can attack it. When placing a queen,
    we increment attack counts for all cells in its row, diagonals. When
    backtracking, we decrement those counts.
    
    Attributes:
        n: Size of the chessboard
        board: 2D array where board[row][col] = attack count (0 = safe, >0 = attacked)
        solution: List of column positions for each queen (solution[row] = col)
        verbose: Whether to print progress
    """

    def __init__(self, n: int, verbose: bool = False):
        """Initialize the solver with attack tracking.
        
        Args:
            n: Size of the chessboard
            verbose: Enable verbose output
            
        Raises:
            ValueError: If n < 1
        """
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        # board[row][col] = number of queens attacking this position
        self.board: List[List[int]] = [[0] * n for _ in range(n)]
        self.solution: List[int] = [-1] * n  # solution[col] = row
        self.verbose = verbose

    def solve(self) -> bool:
        """Solve the N-Queens problem and display result.
        
        Returns:
            True if solution found, False otherwise
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
        """Place queens column by column with attack tracking.
        
        Args:
            col: Current column to place a queen
            
        Returns:
            True if all queens placed successfully, False otherwise
        """
        # Base case: all queens placed
        if col >= self.n:
            return True

        # Try each row in current column
        for row in range(self.n):
            # Check if position is safe (not under attack)
            if self.board[row][col] == 0:
                # Place queen and mark attacked cells
                self.solution[col] = row
                self._mark_attacks(row, col, increment=1)
                
                if self.verbose:
                    print(f"Placed queen at ({row}, {col})")

                # Recursively place remaining queens
                if self._backtrack(col + 1):
                    return True

                # Backtrack: remove queen and unmark attacks
                self._mark_attacks(row, col, increment=-1)
                self.solution[col] = -1
                
                if self.verbose:
                    print(f"Backtracked from ({row}, {col})")

        return False

    def _mark_attacks(self, row: int, col: int, increment: int) -> None:
        """Mark or unmark cells attacked by queen at (row, col).
        
        Args:
            row: Row position of queen
            col: Column position of queen
            increment: 1 to mark attacks, -1 to unmark
        """
        # Mark entire row (only to the right, left is already processed)
        for c in range(col + 1, self.n):
            self.board[row][c] += increment

        # Mark diagonals (only to the right)
        # Upper-right diagonal
        r, c = row - 1, col + 1
        while r >= 0 and c < self.n:
            self.board[r][c] += increment
            r -= 1
            c += 1

        # Lower-right diagonal
        r, c = row + 1, col + 1
        while r < self.n and c < self.n:
            self.board[r][c] += increment
            r += 1
            c += 1

    def _print_board(self) -> None:
        """Print the chessboard solution."""
        print("\\n" + "=" * (4 * self.n + 1))
        for row in range(self.n):
            print("|", end="")
            for col in range(self.n):
                if self.solution[col] == row:
                    print(" Q ", end="|")
                else:
                    print("   ", end="|")
            print()
            print("=" * (4 * self.n + 1))
        print(f"\\nSolution found for {self.n}-Queens problem!\\n")

    def get_solution(self) -> Optional[List[int]]:
        """Get solution as list of row positions.
        
        Returns:
            List where index is column, value is row, or None if not solved
        """
        if -1 in self.solution:
            return None
        return list(self.solution)

    def print_attack_board(self) -> None:
        """Print board showing attack counts (for debugging)."""
        print("\\nAttack count board:")
        for row in range(self.n):
            for col in range(self.n):
                if self.solution[col] == row:
                    print(" Q ", end="")
                else:
                    print(f" {self.board[row][col]} ", end="")
            print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Solve N-Queens using attack cell tracking.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python n_queens_attack_tracking.py 8          # Solve 8-Queens
  python n_queens_attack_tracking.py 20 -v     # Solve with verbose output
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
    
    if args.n < 1:
        print("Error: Board size must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.n in [2, 3]:
        print(f"Warning: No solution exists for {args.n}-Queens problem.")
    
    try:
        solver = NQueensSolverWithTracking(args.n, verbose=args.verbose)
        solver.solve()
    except KeyboardInterrupt:
        print("\\n\\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
