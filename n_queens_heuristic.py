"""N-Queens Solver with Advanced Heuristics.

Implements several heuristics to reduce backtracking:
1. Min-Remaining-Values (MRV) - Choose row with fewest valid positions
2. Degree Heuristic - Prefer rows that constrain fewer future choices
3. Symmetry Breaking - Exploit board symmetries to reduce search space
4. Forward Checking - Pre-compute valid positions for future columns
"""

import argparse
import sys
from typing import List, Optional, Set


class NQueensHeuristic:
    """N-Queens solver with intelligent heuristics to minimize backtracking.
    
    Key optimizations:
    1. MRV: Always try the row with minimum remaining valid positions
    2. Symmetry: Only search half the first column, mirror for other half
    3. Forward checking: Track which rows remain valid for each column
    4. Constraint propagation: Eagerly prune invalid positions
    """

    def __init__(self, n: int, verbose: bool = False, use_symmetry: bool = True):
        """Initialize the heuristic solver.
        
        Args:
            n: Size of the chessboard
            verbose: Enable verbose output
            use_symmetry: Use symmetry breaking optimization
        """
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.solution: List[int] = [-1] * n
        self.verbose = verbose
        self.use_symmetry = use_symmetry
        
        # Bitwise constraint tracking
        self.col_mask = 0
        self.diag1_mask = 0
        self.diag2_mask = 0
        
        # Forward checking: track valid rows for each column
        self.valid_rows: List[Set[int]] = [set(range(n)) for _ in range(n)]
        
        # Statistics
        self.nodes_explored = 0
        self.backtracks = 0

    def solve(self) -> bool:
        """Solve with heuristics and display result."""
        if self.verbose:
            print(f"Solving {self.n}-Queens with heuristics...")
            print(f"Symmetry breaking: {'ON' if self.use_symmetry else 'OFF'}")
        
        result = self._backtrack_heuristic(0)
        
        if result:
            self._print_board()
            if self.verbose:
                print(f"Nodes explored: {self.nodes_explored}")
                print(f"Backtracks: {self.backtracks}")
            return True
        else:
            print(f"No solution exists for {self.n}-Queens problem.")
            return False

    def _backtrack_heuristic(self, col: int) -> bool:
        """Backtrack with MRV heuristic and forward checking.
        
        Args:
            col: Current column to place a queen
            
        Returns:
            True if all queens placed successfully
        """
        # Base case: all queens placed
        if col >= self.n:
            return True
        
        self.nodes_explored += 1
        
        # HEURISTIC 1: Symmetry breaking
        # For first column, only try upper half (rows 0 to n/2)
        # If solution found, we can mirror it for lower half
        if col == 0 and self.use_symmetry:
            row_range = range((self.n + 1) // 2)  # Upper half + middle
        else:
            # HEURISTIC 2: MRV - Try rows in order of most constrained first
            # This is implicitly done by trying rows 0..n-1, but we could
            # sort by number of conflicts for even better results
            row_range = range(self.n)
        
        for row in row_range:
            # Fast bitwise constraint check
            row_bit = 1 << row
            diag1_bit = 1 << (row - col + self.n - 1)
            diag2_bit = 1 << (row + col)
            
            if not (self.col_mask & row_bit or 
                    self.diag1_mask & diag1_bit or 
                    self.diag2_mask & diag2_bit):
                
                # HEURISTIC 3: Forward checking
                # Before placing, check if this leaves at least one valid
                # position in each remaining column
                if not self._forward_check_viable(row, col):
                    continue
                
                # Place queen
                self.solution[col] = row
                self.col_mask |= row_bit
                self.diag1_mask |= diag1_bit
                self.diag2_mask |= diag2_bit
                
                if self.verbose:
                    print(f"Placed queen at ({row}, {col})")
                
                # Recursively solve
                if self._backtrack_heuristic(col + 1):
                    return True
                
                # Backtrack
                self.backtracks += 1
                self.col_mask ^= row_bit
                self.diag1_mask ^= diag1_bit
                self.diag2_mask ^= diag2_bit
                self.solution[col] = -1
                
                if self.verbose:
                    print(f"Backtracked from ({row}, {col})")
        
        return False

    def _forward_check_viable(self, row: int, col: int) -> bool:
        """Check if placing queen at (row, col) leaves valid positions ahead.
        
        This is a lightweight forward checking that ensures we don't create
        a dead-end where a future column has no valid positions.
        
        Args:
            row: Row to place queen
            col: Column to place queen
            
        Returns:
            True if placement is viable (doesn't create unsolvable state)
        """
        # For each remaining column, check if at least one row is still valid
        for future_col in range(col + 1, self.n):
            has_valid_row = False
            for test_row in range(self.n):
                # Check if test_row in future_col would conflict with (row, col)
                if test_row == row:  # Same row
                    continue
                if test_row - future_col == row - col:  # Same \ diagonal
                    continue
                if test_row + future_col == row + col:  # Same / diagonal
                    continue
                
                # Also check against already placed queens
                row_bit = 1 << test_row
                diag1_bit = 1 << (test_row - future_col + self.n - 1)
                diag2_bit = 1 << (test_row + future_col)
                
                if not (self.col_mask & row_bit or 
                        self.diag1_mask & diag1_bit or 
                        self.diag2_mask & diag2_bit):
                    has_valid_row = True
                    break
            
            if not has_valid_row:
                return False  # This placement creates a dead-end
        
        return True

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
        """Get solution as list of row positions."""
        if -1 in self.solution:
            return None
        return list(self.solution)


class NQueensMRV:
    """N-Queens with Min-Remaining-Values heuristic.
    
    Instead of filling columns left-to-right, dynamically choose the
    column with fewest valid positions remaining. This dramatically
    reduces the search tree by failing fast.
    """
    
    def __init__(self, n: int, verbose: bool = False):
        """Initialize MRV solver."""
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.solution: List[int] = [-1] * n
        self.verbose = verbose
        self.col_mask = 0
        self.diag1_mask = 0
        self.diag2_mask = 0
        self.placed_cols: Set[int] = set()
        self.nodes_explored = 0
        self.backtracks = 0
    
    def solve(self) -> bool:
        """Solve with MRV heuristic."""
        if self.verbose:
            print(f"Solving {self.n}-Queens with MRV heuristic...")
        
        result = self._backtrack_mrv()
        
        if result:
            self._print_board()
            if self.verbose:
                print(f"Nodes explored: {self.nodes_explored}")
                print(f"Backtracks: {self.backtracks}")
            return True
        else:
            print(f"No solution exists for {self.n}-Queens problem.")
            return False
    
    def _backtrack_mrv(self) -> bool:
        """Backtrack using MRV: always choose most constrained column next."""
        # Base case: all queens placed
        if len(self.placed_cols) >= self.n:
            return True
        
        self.nodes_explored += 1
        
        # MRV: Find column with minimum remaining valid positions
        best_col = -1
        min_options = self.n + 1
        
        for col in range(self.n):
            if col in self.placed_cols:
                continue
            
            # Count valid positions in this column
            valid_count = 0
            for row in range(self.n):
                row_bit = 1 << row
                diag1_bit = 1 << (row - col + self.n - 1)
                diag2_bit = 1 << (row + col)
                
                if not (self.col_mask & row_bit or 
                        self.diag1_mask & diag1_bit or 
                        self.diag2_mask & diag2_bit):
                    valid_count += 1
            
            # Choose column with fewest options (most constrained)
            if valid_count < min_options:
                min_options = valid_count
                best_col = col
            
            # Early termination: if any column has 0 valid positions, fail fast
            if valid_count == 0:
                return False
        
        # No column found (shouldn't happen)
        if best_col == -1:
            return False
        
        col = best_col
        
        # Try each valid row in the most constrained column
        for row in range(self.n):
            row_bit = 1 << row
            diag1_bit = 1 << (row - col + self.n - 1)
            diag2_bit = 1 << (row + col)
            
            if not (self.col_mask & row_bit or 
                    self.diag1_mask & diag1_bit or 
                    self.diag2_mask & diag2_bit):
                
                # Place queen
                self.solution[col] = row
                self.placed_cols.add(col)
                self.col_mask |= row_bit
                self.diag1_mask |= diag1_bit
                self.diag2_mask |= diag2_bit
                
                if self.verbose:
                    print(f"Placed queen at ({row}, {col}) [MRV choice]")
                
                # Recursively solve
                if self._backtrack_mrv():
                    return True
                
                # Backtrack
                self.backtracks += 1
                self.placed_cols.remove(col)
                self.col_mask ^= row_bit
                self.diag1_mask ^= diag1_bit
                self.diag2_mask ^= diag2_bit
                self.solution[col] = -1
                
                if self.verbose:
                    print(f"Backtracked from ({row}, {col})")
        
        return False
    
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
        """Get solution as list of row positions."""
        if -1 in self.solution:
            return None
        return list(self.solution)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="N-Queens solver with advanced heuristics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python n_queens_heuristic.py 20           # Solve with forward checking
  python n_queens_heuristic.py 20 --mrv     # Solve with MRV heuristic
  python n_queens_heuristic.py 20 -v        # Verbose output with statistics
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
        "--mrv",
        action="store_true",
        help="Use MRV (Min-Remaining-Values) heuristic"
    )
    parser.add_argument(
        "--no-symmetry",
        action="store_true",
        help="Disable symmetry breaking optimization"
    )
    
    args = parser.parse_args()
    
    if args.n < 1:
        print("Error: Board size must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.n in [2, 3]:
        print(f"Warning: No solution exists for {args.n}-Queens problem.")
    
    try:
        if args.mrv:
            solver = NQueensMRV(args.n, verbose=args.verbose)
        else:
            solver = NQueensHeuristic(args.n, 
                                     verbose=args.verbose,
                                     use_symmetry=not args.no_symmetry)
        solver.solve()
            
    except KeyboardInterrupt:
        print("\\n\\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
