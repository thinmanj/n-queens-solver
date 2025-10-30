"""N-Queens Solver: Hybrid Bitwise + Attack Tracking.

Combines bitwise operations for O(1) constraint checking with
2D board attack tracking for visualization and debugging.
"""

import argparse
import sys
from typing import List, Optional


class NQueensHybrid:
    """Hybrid solver using bitwise constraints + 2D attack board.
    
    Uses bitwise masks for fast O(1) constraint checking during solving,
    but also maintains a 2D attack board for visualization and debugging.
    
    Attributes:
        n: Size of the chessboard
        board: 2D array tracking attack counts (for visualization)
        solution: List of row positions for each queen
        col_mask: Bitmask of occupied rows
        diag1_mask: Bitmask of occupied positive diagonals
        diag2_mask: Bitmask of occupied negative diagonals
        verbose: Whether to print progress
    """

    def __init__(self, n: int, verbose: bool = False, track_attacks: bool = False):
        """Initialize the hybrid solver.
        
        Args:
            n: Size of the chessboard
            verbose: Enable verbose output
            track_attacks: Maintain 2D attack board (slower but visualizable)
            
        Raises:
            ValueError: If n < 1
        """
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.solution: List[int] = [-1] * n
        self.track_attacks = track_attacks
        
        # Bitwise constraint tracking (always used for fast checking)
        self.col_mask = 0
        self.diag1_mask = 0
        self.diag2_mask = 0
        
        # Optional 2D board for visualization
        if track_attacks:
            self.board: List[List[int]] = [[0] * n for _ in range(n)]
        
        self.verbose = verbose

    def solve(self) -> bool:
        """Solve the N-Queens problem and display result.
        
        Returns:
            True if solution found, False otherwise
        """
        if self.verbose:
            print(f"Solving {self.n}-Queens problem...")
            print(f"Attack tracking: {'ON' if self.track_attacks else 'OFF'}")
        
        if self._backtrack(0):
            self._print_board()
            return True
        else:
            print(f"No solution exists for {self.n}-Queens problem.")
            return False

    def _backtrack(self, col: int) -> bool:
        """Place queens using bitwise constraints + optional attack tracking.
        
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
            # FAST PATH: O(1) bitwise constraint check
            row_bit = 1 << row
            diag1_bit = 1 << (row - col + self.n - 1)
            diag2_bit = 1 << (row + col)
            
            if not (self.col_mask & row_bit or 
                    self.diag1_mask & diag1_bit or 
                    self.diag2_mask & diag2_bit):
                
                # Place queen
                self.solution[col] = row
                self.col_mask |= row_bit
                self.diag1_mask |= diag1_bit
                self.diag2_mask |= diag2_bit
                
                # Optional: track attacks on 2D board
                if self.track_attacks:
                    self._mark_attacks(row, col, increment=1)
                
                if self.verbose:
                    print(f"Placed queen at ({row}, {col})")
                    if self.track_attacks:
                        self.print_attack_board()

                # Recursively place remaining queens
                if self._backtrack(col + 1):
                    return True

                # Backtrack: remove queen and constraints
                self.col_mask ^= row_bit
                self.diag1_mask ^= diag1_bit
                self.diag2_mask ^= diag2_bit
                
                if self.track_attacks:
                    self._mark_attacks(row, col, increment=-1)
                
                self.solution[col] = -1
                
                if self.verbose:
                    print(f"Backtracked from ({row}, {col})")

        return False

    def _mark_attacks(self, row: int, col: int, increment: int) -> None:
        """Mark or unmark cells attacked by queen (for visualization only).
        
        Args:
            row: Row position of queen
            col: Column position of queen
            increment: 1 to mark attacks, -1 to unmark
        """
        # Mark row (only to the right)
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

    def print_attack_board(self) -> None:
        """Print board showing attack counts (requires track_attacks=True)."""
        if not self.track_attacks:
            print("Attack tracking is disabled. Enable with track_attacks=True")
            return
        
        print("\\nAttack count board:")
        for row in range(self.n):
            for col in range(self.n):
                if self.solution[col] == row:
                    print(" Q ", end="")
                else:
                    print(f" {self.board[row][col]} ", end="")
            print()
        print()

    def get_solution(self) -> Optional[List[int]]:
        """Get solution as list of row positions.
        
        Returns:
            List where index is column, value is row, or None if not solved
        """
        if -1 in self.solution:
            return None
        return list(self.solution)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Hybrid N-Queens solver: bitwise + attack tracking.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python n_queens_hybrid.py 8              # Fast solve with bitwise only
  python n_queens_hybrid.py 8 -t           # Solve with attack board tracking
  python n_queens_hybrid.py 8 -t -v        # Verbose with attack visualization
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
    parser.add_argument(
        "-t", "--track-attacks",
        action="store_true",
        help="Track attacks on 2D board (slower but visualizable)"
    )
    
    args = parser.parse_args()
    
    if args.n < 1:
        print("Error: Board size must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.n in [2, 3]:
        print(f"Warning: No solution exists for {args.n}-Queens problem.")
    
    try:
        solver = NQueensHybrid(args.n, 
                               verbose=args.verbose, 
                               track_attacks=args.track_attacks)
        solver.solve()
        
        # Show final attack board if tracking is enabled
        if args.track_attacks and not args.verbose:
            solver.print_attack_board()
            
    except KeyboardInterrupt:
        print("\\n\\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
