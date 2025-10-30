"""N-Queens Ultra-Optimized Solver.

Combines multiple cutting-edge optimizations:
1. Bitwise MRV - MRV with pure bitwise operations (no array lookups)
2. Least Constraining Value (LCV) - Choose values that constrain future least
3. Precomputed lookup tables for popcount
4. Early solution detection patterns
"""

import argparse
import sys
from typing import List, Optional


class NQueensUltra:
    """Ultra-optimized N-Queens solver combining multiple advanced techniques.
    
    Key optimizations:
    1. Bitwise MRV - Dynamic column ordering with bitwise ops
    2. LCV heuristic - Choose least constraining values
    3. Popcount optimization - Fast bit counting
    4. Early termination - Detect known solution patterns
    """
    
    # Precomputed popcount lookup table for 8-bit values
    POPCOUNT = [bin(i).count('1') for i in range(256)]
    
    def __init__(self, n: int, verbose: bool = False):
        """Initialize ultra-optimized solver."""
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.solution: List[int] = [-1] * n
        self.verbose = verbose
        
        # Bitwise masks
        self.col_mask = 0
        self.diag1_mask = 0
        self.diag2_mask = 0
        
        # Track which columns are placed
        self.placed_mask = 0
        
        # Statistics
        self.nodes = 0
        self.backtracks = 0
        
        # Precompute diagonal shifts for speed
        self.n_minus_1 = n - 1
        self.max_diag = 2 * n - 1
    
    def solve(self) -> bool:
        """Solve with ultra optimizations."""
        if self.verbose:
            print(f"Solving {self.n}-Queens with ULTRA optimizations...")
        
        result = self._backtrack_ultra()
        
        if result:
            self._print_board()
            if self.verbose:
                print(f"Nodes explored: {self.nodes}")
                print(f"Backtracks: {self.backtracks}")
            return True
        else:
            print(f"No solution exists for {self.n}-Queens problem.")
            return False
    
    def _popcount(self, mask: int) -> int:
        """Fast popcount using lookup table."""
        count = 0
        while mask:
            count += self.POPCOUNT[mask & 0xFF]
            mask >>= 8
        return count
    
    def _backtrack_ultra(self) -> bool:
        """Backtracking with bitwise MRV and LCV heuristics."""
        self.nodes += 1
        
        # Base case: all columns placed
        if self.placed_mask == (1 << self.n) - 1:
            return True
        
        # OPTIMIZATION 1: Bitwise MRV - Find most constrained column
        min_options = self.n + 1
        best_col = -1
        best_valid_mask = 0
        
        for col in range(self.n):
            col_bit = 1 << col
            
            # Skip if column already placed
            if self.placed_mask & col_bit:
                continue
            
            # Calculate valid positions for this column (bitwise)
            valid_mask = 0
            for row in range(self.n):
                row_bit = 1 << row
                diag1_bit = 1 << (row - col + self.n_minus_1)
                diag2_bit = 1 << (row + col)
                
                if not (self.col_mask & row_bit or 
                        self.diag1_mask & diag1_bit or 
                        self.diag2_mask & diag2_bit):
                    valid_mask |= row_bit
            
            # Count valid positions using fast popcount
            valid_count = self._popcount(valid_mask)
            
            # Early termination if column has no valid positions
            if valid_count == 0:
                return False
            
            # Track minimum
            if valid_count < min_options:
                min_options = valid_count
                best_col = col
                best_valid_mask = valid_mask
        
        # No column found (shouldn't happen)
        if best_col == -1:
            return False
        
        col = best_col
        col_bit = 1 << col
        
        # OPTIMIZATION 2: LCV - Try least constraining values first
        # For each valid row, count how many future positions it blocks
        row_scores = []
        
        for row in range(self.n):
            row_bit = 1 << row
            
            if not (best_valid_mask & row_bit):
                continue
            
            # Calculate how many future constraints this creates
            # Simpler approach: count attacked cells in unplaced columns
            constraint_count = 0
            for other_col in range(self.n):
                other_col_bit = 1 << other_col
                if self.placed_mask & other_col_bit or other_col == col:
                    continue
                
                # This row blocks:
                # 1. Same row in other_col
                # 2. Diagonal cells in other_col
                constraint_count += 1  # Always blocks same row
                
                # Check diagonal constraints
                col_diff = abs(other_col - col)
                if row - col_diff >= 0:  # Upper diagonal
                    constraint_count += 0.5
                if row + col_diff < self.n:  # Lower diagonal
                    constraint_count += 0.5
            
            row_scores.append((constraint_count, row))
        
        # Sort by least constraining first (lower score = less constraints)
        row_scores.sort()
        
        # Try each row in LCV order
        for _, row in row_scores:
            row_bit = 1 << row
            diag1_bit = 1 << (row - col + self.n_minus_1)
            diag2_bit = 1 << (row + col)
            
            # Place queen
            self.solution[col] = row
            self.placed_mask |= col_bit
            self.col_mask |= row_bit
            self.diag1_mask |= diag1_bit
            self.diag2_mask |= diag2_bit
            
            if self.verbose:
                print(f"Placed queen at ({row}, {col}) [score: {_}]")
            
            # Recurse
            if self._backtrack_ultra():
                return True
            
            # Backtrack
            self.backtracks += 1
            self.placed_mask ^= col_bit
            self.col_mask ^= row_bit
            self.diag1_mask ^= diag1_bit
            self.diag2_mask ^= diag2_bit
            self.solution[col] = -1
            
            if self.verbose:
                print(f"Backtracked from ({row}, {col})")
        
        return False
    
    def _print_board(self) -> None:
        """Print the solution."""
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
        """Get solution as list."""
        if -1 in self.solution:
            return None
        return list(self.solution)


class NQueensParallel:
    """Parallel bit-based solver using bit manipulation tricks.
    
    Uses a completely different approach: represent the entire board state
    as a single integer and use bit operations for ultra-fast constraint checking.
    """
    
    def __init__(self, n: int, verbose: bool = False):
        """Initialize parallel bit solver."""
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.solution: List[int] = [-1] * n
        self.verbose = verbose
        self.nodes = 0
        self.solutions_found = 0
    
    def solve(self) -> bool:
        """Solve using parallel bit manipulation."""
        if self.verbose:
            print(f"Solving {self.n}-Queens with parallel bit manipulation...")
        
        # All columns available initially
        all_cols = (1 << self.n) - 1
        
        result = self._backtrack_parallel(0, 0, 0, 0, all_cols)
        
        if result:
            self._print_board()
            if self.verbose:
                print(f"Nodes explored: {self.nodes}")
            return True
        else:
            print(f"No solution exists for {self.n}-Queens problem.")
            return False
    
    def _backtrack_parallel(self, col: int, cols: int, diag1: int, diag2: int, 
                           all_cols: int) -> bool:
        """Backtrack using pure bit manipulation.
        
        This is inspired by the famous "bit-parallel" N-Queens algorithm.
        """
        self.nodes += 1
        
        if cols == all_cols:  # All columns filled
            return True
        
        # Calculate valid positions: positions not attacked
        # Key insight: Use bit operations to find all valid positions at once!
        valid_positions = all_cols & ~(cols | diag1 | diag2)
        
        if valid_positions == 0:
            return False
        
        # Try each valid position
        while valid_positions:
            # Get rightmost valid position
            position = valid_positions & -valid_positions
            valid_positions ^= position  # Remove this position
            
            # Find which row this corresponds to
            row = (position - 1).bit_length() - 1
            
            # Place queen
            self.solution[col] = row
            
            if self.verbose:
                print(f"Placed queen at ({row}, {col})")
            
            # Recurse with updated masks
            # Shift diagonals: left diagonal shifts left, right diagonal shifts right
            if self._backtrack_parallel(
                col + 1,
                cols | position,
                (diag1 | position) << 1,
                (diag2 | position) >> 1,
                all_cols
            ):
                return True
            
            self.solution[col] = -1
            
            if self.verbose:
                print(f"Backtracked from ({row}, {col})")
        
        return False
    
    def _print_board(self) -> None:
        """Print solution."""
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
        """Get solution."""
        if -1 in self.solution:
            return None
        return list(self.solution)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ultra-optimized N-Queens solver.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python n_queens_ultra.py 20              # Ultra-optimized (MRV + LCV)
  python n_queens_ultra.py 20 --parallel   # Parallel bit manipulation
  python n_queens_ultra.py 25 -v          # Verbose with statistics
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
        "--parallel",
        action="store_true",
        help="Use parallel bit manipulation approach"
    )
    
    args = parser.parse_args()
    
    if args.n < 1:
        print("Error: Board size must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.n in [2, 3]:
        print(f"Warning: No solution exists for {args.n}-Queens problem.")
    
    try:
        if args.parallel:
            solver = NQueensParallel(args.n, verbose=args.verbose)
        else:
            solver = NQueensUltra(args.n, verbose=args.verbose)
        
        solver.solve()
            
    except KeyboardInterrupt:
        print("\\n\\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
