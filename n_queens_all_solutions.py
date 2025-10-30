"""N-Queens All Solutions Finder.

Find ALL solutions to the N-Queens problem with various optimization strategies.
"""

import argparse
import sys
import time
from typing import List, Set


class NQueensAllSolutions:
    """Find all solutions using standard backtracking."""
    
    def __init__(self, n: int, verbose: bool = False, unique_only: bool = False):
        """Initialize solver.
        
        Args:
            n: Board size
            verbose: Show progress
            unique_only: Only count fundamentally unique solutions (no rotations/reflections)
        """
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.verbose = verbose
        self.unique_only = unique_only
        
        # Bitwise masks
        self.col_mask = 0
        self.diag1_mask = 0
        self.diag2_mask = 0
        
        # Store all solutions
        self.solutions: List[List[int]] = []
        self.unique_solutions: Set[tuple] = set()
        
        # Statistics
        self.nodes_explored = 0
    
    def solve_all(self) -> List[List[int]]:
        """Find all solutions."""
        start_time = time.time()
        
        if self.verbose:
            print(f"Finding all solutions for {self.n}-Queens...")
        
        self._backtrack(0, [-1] * self.n)
        
        elapsed = time.time() - start_time
        
        if self.unique_only:
            count = len(self.unique_solutions)
        else:
            count = len(self.solutions)
        
        print(f"\nFound {count} {'unique ' if self.unique_only else ''}solutions")
        print(f"Time: {elapsed:.4f}s")
        print(f"Nodes explored: {self.nodes_explored}")
        
        return self.solutions
    
    def _backtrack(self, col: int, board: List[int]) -> None:
        """Backtrack through all possibilities."""
        self.nodes_explored += 1
        
        # Base case: found a solution
        if col >= self.n:
            if self.unique_only:
                canonical = self._get_canonical_form(board)
                if canonical not in self.unique_solutions:
                    self.unique_solutions.add(canonical)
                    self.solutions.append(list(board))
            else:
                self.solutions.append(list(board))
            
            if self.verbose and len(self.solutions) % 10 == 0:
                print(f"Found {len(self.solutions)} solutions...")
            return
        
        # Try each row in current column
        for row in range(self.n):
            row_bit = 1 << row
            diag1_bit = 1 << (row - col + self.n - 1)
            diag2_bit = 1 << (row + col)
            
            if not (self.col_mask & row_bit or 
                    self.diag1_mask & diag1_bit or 
                    self.diag2_mask & diag2_bit):
                
                # Place queen
                board[col] = row
                self.col_mask |= row_bit
                self.diag1_mask |= diag1_bit
                self.diag2_mask |= diag2_bit
                
                # Recurse
                self._backtrack(col + 1, board)
                
                # Backtrack
                self.col_mask ^= row_bit
                self.diag1_mask ^= diag1_bit
                self.diag2_mask ^= diag2_bit
                board[col] = -1
    
    def _get_canonical_form(self, board: List[int]) -> tuple:
        """Get canonical form considering rotations and reflections."""
        # Generate all 8 symmetries (4 rotations × 2 reflections)
        forms = [
            tuple(board),  # Original
            tuple(self._rotate_90(board)),
            tuple(self._rotate_180(board)),
            tuple(self._rotate_270(board)),
            tuple(self._reflect_horizontal(board)),
            tuple(self._reflect_vertical(board)),
            tuple(self._reflect_diagonal(board)),
            tuple(self._reflect_anti_diagonal(board)),
        ]
        # Return lexicographically smallest (canonical)
        return min(forms)
    
    def _rotate_90(self, board: List[int]) -> List[int]:
        """Rotate board 90 degrees clockwise."""
        return [self.n - 1 - col for col, row in sorted(enumerate(board), key=lambda x: x[1])]
    
    def _rotate_180(self, board: List[int]) -> List[int]:
        """Rotate board 180 degrees."""
        return [self.n - 1 - row for row in reversed(board)]
    
    def _rotate_270(self, board: List[int]) -> List[int]:
        """Rotate board 270 degrees clockwise."""
        return [col for col, row in sorted(enumerate(board), key=lambda x: -x[1])]
    
    def _reflect_horizontal(self, board: List[int]) -> List[int]:
        """Reflect horizontally (flip left-right)."""
        return list(reversed(board))
    
    def _reflect_vertical(self, board: List[int]) -> List[int]:
        """Reflect vertically (flip up-down)."""
        return [self.n - 1 - row for row in board]
    
    def _reflect_diagonal(self, board: List[int]) -> List[int]:
        """Reflect across main diagonal."""
        result = [-1] * self.n
        for col, row in enumerate(board):
            result[row] = col
        return result
    
    def _reflect_anti_diagonal(self, board: List[int]) -> List[int]:
        """Reflect across anti-diagonal."""
        result = [-1] * self.n
        for col, row in enumerate(board):
            result[self.n - 1 - row] = self.n - 1 - col
        return result


class NQueensAllSolutionsSymmetry:
    """Find all solutions using symmetry breaking to reduce search space."""
    
    def __init__(self, n: int, verbose: bool = False):
        """Initialize solver with symmetry breaking."""
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.verbose = verbose
        
        # Bitwise masks
        self.col_mask = 0
        self.diag1_mask = 0
        self.diag2_mask = 0
        
        # Store all solutions
        self.solutions: List[List[int]] = []
        self.nodes_explored = 0
    
    def solve_all(self) -> List[List[int]]:
        """Find all unique solutions using symmetry breaking."""
        start_time = time.time()
        
        if self.verbose:
            print(f"Finding all solutions with symmetry breaking for {self.n}-Queens...")
        
        # OPTIMIZATION: Only search upper half of first column
        # Then generate symmetric solutions
        board = [-1] * self.n
        
        # Search upper half + middle
        for first_row in range((self.n + 1) // 2):
            row_bit = 1 << first_row
            diag1_bit = 1 << (first_row + self.n - 1)
            diag2_bit = 1 << first_row
            
            board[0] = first_row
            self.col_mask = row_bit
            self.diag1_mask = diag1_bit
            self.diag2_mask = diag2_bit
            
            self._backtrack(1, board, is_middle=(first_row == self.n // 2 and self.n % 2 == 1))
            
            # Reset
            self.col_mask = 0
            self.diag1_mask = 0
            self.diag2_mask = 0
            board[0] = -1
        
        elapsed = time.time() - start_time
        
        print(f"\nFound {len(self.solutions)} total solutions (using symmetry)")
        print(f"Time: {elapsed:.4f}s")
        print(f"Nodes explored: {self.nodes_explored}")
        
        return self.solutions
    
    def _backtrack(self, col: int, board: List[int], is_middle: bool = False) -> None:
        """Backtrack with symmetry awareness."""
        self.nodes_explored += 1
        
        if col >= self.n:
            # Found a solution
            self.solutions.append(list(board))
            
            # Generate symmetric solution (unless first queen is in middle)
            if not is_middle:
                symmetric = [self.n - 1 - row for row in reversed(board)]
                self.solutions.append(symmetric)
            
            if self.verbose and len(self.solutions) % 10 == 0:
                print(f"Found {len(self.solutions)} solutions...")
            return
        
        for row in range(self.n):
            row_bit = 1 << row
            diag1_bit = 1 << (row - col + self.n - 1)
            diag2_bit = 1 << (row + col)
            
            if not (self.col_mask & row_bit or 
                    self.diag1_mask & diag1_bit or 
                    self.diag2_mask & diag2_bit):
                
                board[col] = row
                self.col_mask |= row_bit
                self.diag1_mask |= diag1_bit
                self.diag2_mask |= diag2_bit
                
                self._backtrack(col + 1, board, is_middle)
                
                self.col_mask ^= row_bit
                self.diag1_mask ^= diag1_bit
                self.diag2_mask ^= diag2_bit
                board[col] = -1


class NQueensAllSolutionsParallel:
    """Find all solutions with parallel bit manipulation (ultra fast)."""
    
    def __init__(self, n: int, verbose: bool = False):
        """Initialize parallel solver."""
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.verbose = verbose
        self.solutions: List[List[int]] = []
        self.nodes_explored = 0
    
    def solve_all(self) -> List[List[int]]:
        """Find all solutions using parallel bit operations."""
        start_time = time.time()
        
        if self.verbose:
            print(f"Finding all solutions with parallel bits for {self.n}-Queens...")
        
        all_cols = (1 << self.n) - 1
        board = [-1] * self.n
        
        self._backtrack_parallel(0, 0, 0, 0, all_cols, board)
        
        elapsed = time.time() - start_time
        
        print(f"\nFound {len(self.solutions)} solutions (parallel)")
        print(f"Time: {elapsed:.4f}s")
        print(f"Nodes explored: {self.nodes_explored}")
        
        return self.solutions
    
    def _backtrack_parallel(self, col: int, cols: int, diag1: int, diag2: int,
                           all_cols: int, board: List[int]) -> None:
        """Backtrack using parallel bit operations."""
        self.nodes_explored += 1
        
        if cols == all_cols:
            self.solutions.append(list(board))
            if self.verbose and len(self.solutions) % 10 == 0:
                print(f"Found {len(self.solutions)} solutions...")
            return
        
        # Find all valid positions at once
        valid_positions = all_cols & ~(cols | diag1 | diag2)
        
        while valid_positions:
            position = valid_positions & -valid_positions
            valid_positions ^= position
            
            row = (position - 1).bit_length() - 1
            board[col] = row
            
            self._backtrack_parallel(
                col + 1,
                cols | position,
                (diag1 | position) << 1,
                (diag2 | position) >> 1,
                all_cols,
                board
            )
            
            board[col] = -1


def print_solution(board: List[int]) -> None:
    """Print a single solution."""
    n = len(board)
    print("=" * (4 * n + 1))
    for row in range(n):
        print("|", end="")
        for col in range(n):
            if board[col] == row:
                print(" Q ", end="|")
            else:
                print("   ", end="|")
        print()
        print("=" * (4 * n + 1))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Find ALL solutions to N-Queens problem.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python n_queens_all_solutions.py 8                  # Find all solutions
  python n_queens_all_solutions.py 8 --unique         # Find unique solutions only
  python n_queens_all_solutions.py 8 --symmetry       # Use symmetry breaking
  python n_queens_all_solutions.py 8 --parallel       # Parallel bit manipulation
  python n_queens_all_solutions.py 8 --show           # Display all solutions
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
        help="Show progress"
    )
    parser.add_argument(
        "--unique",
        action="store_true",
        help="Only count fundamentally unique solutions (no rotations/reflections)"
    )
    parser.add_argument(
        "--symmetry",
        action="store_true",
        help="Use symmetry breaking optimization"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Use parallel bit manipulation"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display all solutions (only for small N)"
    )
    
    args = parser.parse_args()
    
    if args.n < 1:
        print("Error: Board size must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.n in [2, 3]:
        print(f"No solutions exist for {args.n}-Queens problem.")
        return
    
    try:
        if args.parallel:
            solver = NQueensAllSolutionsParallel(args.n, verbose=args.verbose)
        elif args.symmetry:
            solver = NQueensAllSolutionsSymmetry(args.n, verbose=args.verbose)
        else:
            solver = NQueensAllSolutions(args.n, verbose=args.verbose, 
                                        unique_only=args.unique)
        
        solutions = solver.solve_all()
        
        if args.show and len(solutions) <= 20:
            print("\nAll solutions:")
            for i, sol in enumerate(solutions, 1):
                print(f"\nSolution {i}:")
                print_solution(sol)
        elif args.show:
            print(f"\nToo many solutions ({len(solutions)}) to display.")
            print("Showing first 5:")
            for i, sol in enumerate(solutions[:5], 1):
                print(f"\nSolution {i}:")
                print_solution(sol)
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
