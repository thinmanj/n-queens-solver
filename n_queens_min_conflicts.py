#!/usr/bin/env python3
"""
N-Queens Solver using Min-Conflicts Local Search Algorithm.

This approach is excellent for very large N (1000+) but is incomplete
(may not find a solution even if one exists). Uses random restarts.

Time Complexity: O(N) per step (usually finds solution quickly)
Space Complexity: O(N)

Algorithm:
1. Start with random complete assignment (one queen per column)
2. Pick column with conflicts
3. Move queen to row with minimum conflicts
4. Repeat until no conflicts or max steps reached
5. Restart if needed

Author: N-Queens Optimizer
"""

import sys
import time
import random
import argparse
from typing import List, Optional, Set, Tuple


class MinConflictsSolver:
    """N-Queens solver using Min-Conflicts local search."""
    
    def __init__(self, n: int, verbose: bool = False, max_steps: int = None, max_restarts: int = 100):
        """
        Initialize the Min-Conflicts solver.
        
        Args:
            n: Size of the board (number of queens)
            verbose: Enable detailed output
            max_steps: Maximum steps per restart (default: n*n)
            max_restarts: Maximum number of restarts
        """
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.verbose = verbose
        self.max_steps = max_steps if max_steps else n * n
        self.max_restarts = max_restarts
        
        # board[col] = row (complete assignment)
        self.board: List[int] = []
        
        # Statistics
        self.total_steps = 0
        self.restarts_used = 0
        self.nodes_explored = 0
    
    def solve(self) -> bool:
        """
        Solve the N-Queens problem using Min-Conflicts with restarts.
        
        Returns:
            True if solution found, False otherwise
        """
        start_time = time.time()
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Min-Conflicts Solver for {self.n}-Queens")
            print(f"Max steps per restart: {self.max_steps}")
            print(f"Max restarts: {self.max_restarts}")
            print(f"{'='*60}\n")
        
        # Handle trivial cases
        if self.n == 1:
            self.board = [0]
            return True
        
        if self.n in [2, 3]:
            if self.verbose:
                print(f"No solution exists for {self.n}-Queens")
            return False
        
        # Try multiple restarts
        for restart in range(self.max_restarts):
            self.restarts_used = restart + 1
            
            if self.verbose and restart > 0:
                print(f"\nRestart #{restart + 1}")
            
            # Random initial configuration
            self._random_initialization()
            
            # Min-conflicts local search
            if self._min_conflicts_search():
                elapsed = time.time() - start_time
                self._print_statistics(elapsed)
                return True
        
        # Failed to find solution
        elapsed = time.time() - start_time
        if self.verbose:
            print(f"\nFailed to find solution after {self.max_restarts} restarts")
            print(f"Total steps: {self.total_steps}")
            print(f"Time: {elapsed:.4f}s")
        
        return False
    
    def _random_initialization(self) -> None:
        """Initialize board with random queen placement (one per column)."""
        self.board = [random.randint(0, self.n - 1) for _ in range(self.n)]
    
    def _min_conflicts_search(self) -> bool:
        """
        Perform min-conflicts local search.
        
        Returns:
            True if solution found, False if max steps reached
        """
        for step in range(self.max_steps):
            self.total_steps += 1
            self.nodes_explored += 1
            
            # Find columns with conflicts
            conflicted_cols = self._get_conflicted_columns()
            
            if not conflicted_cols:
                # Solution found!
                return True
            
            # Pick random conflicted column
            col = random.choice(conflicted_cols)
            
            # Move queen to row with minimum conflicts
            best_row = self._min_conflict_row(col)
            self.board[col] = best_row
            
            if self.verbose and step % 1000 == 0 and step > 0:
                conflicts = len(conflicted_cols)
                print(f"  Step {step}: {conflicts} columns with conflicts")
        
        return False
    
    def _get_conflicted_columns(self) -> List[int]:
        """
        Get list of columns that have queens in conflict.
        
        Returns:
            List of column indices with conflicts
        """
        conflicted = []
        
        for col in range(self.n):
            if self._count_conflicts(col) > 0:
                conflicted.append(col)
        
        return conflicted
    
    def _count_conflicts(self, col: int) -> int:
        """
        Count how many conflicts the queen in given column has.
        
        Args:
            col: Column index
            
        Returns:
            Number of conflicts
        """
        row = self.board[col]
        conflicts = 0
        
        for other_col in range(self.n):
            if other_col == col:
                continue
            
            other_row = self.board[other_col]
            
            # Check row conflict
            if other_row == row:
                conflicts += 1
            
            # Check diagonal conflicts
            elif abs(other_row - row) == abs(other_col - col):
                conflicts += 1
        
        return conflicts
    
    def _min_conflict_row(self, col: int) -> int:
        """
        Find row with minimum conflicts for given column.
        
        Args:
            col: Column to find best row for
            
        Returns:
            Row index with minimum conflicts
        """
        min_conflicts = self.n + 1
        best_rows = []
        
        # Save current position
        original_row = self.board[col]
        
        # Try each row
        for row in range(self.n):
            self.board[col] = row
            conflicts = self._count_conflicts(col)
            
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_rows = [row]
            elif conflicts == min_conflicts:
                best_rows.append(row)
        
        # Restore original position temporarily
        self.board[col] = original_row
        
        # Return random best row (tie-breaking)
        return random.choice(best_rows)
    
    def get_solution(self) -> List[int]:
        """
        Get the solution as a list of row positions.
        
        Returns:
            List where index is column and value is row
        """
        return self.board.copy()
    
    def _print_board(self) -> None:
        """Print the board configuration."""
        print(f"\nSolution for {self.n}-Queens:")
        
        # For large boards, just show the array
        if self.n > 20:
            print(f"Board: {self.board}")
            return
        
        # Visual representation for smaller boards
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if self.board[col] == row:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        
        print(f"\nSolution array: {self.board}")
    
    def _print_statistics(self, elapsed: float) -> None:
        """Print solving statistics."""
        print(f"\n{'='*60}")
        print(f"Solution found for {self.n}-Queens!")
        print(f"{'='*60}")
        print(f"Restarts used: {self.restarts_used}")
        print(f"Total steps: {self.total_steps}")
        print(f"Nodes explored: {self.nodes_explored}")
        print(f"Time: {elapsed:.4f}s")
        print(f"{'='*60}")
        
        if self.n <= 20:
            self._print_board()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Solve N-Queens using Min-Conflicts local search',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Solve 8-Queens
  %(prog)s 100          # Solve 100-Queens
  %(prog)s 1000 -v      # Solve 1000-Queens with verbose output
  %(prog)s 50 --steps 10000  # Custom max steps per restart
        """
    )
    
    parser.add_argument(
        'N',
        nargs='?',
        type=int,
        default=8,
        help='Size of the board (default: 8)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--steps',
        type=int,
        default=None,
        help='Max steps per restart (default: N*N)'
    )
    
    parser.add_argument(
        '--restarts',
        type=int,
        default=100,
        help='Max number of restarts (default: 100)'
    )
    
    args = parser.parse_args()
    
    try:
        solver = MinConflictsSolver(
            n=args.N,
            verbose=args.verbose,
            max_steps=args.steps,
            max_restarts=args.restarts
        )
        
        success = solver.solve()
        
        if not success:
            print(f"\nFailed to find solution for {args.N}-Queens")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
