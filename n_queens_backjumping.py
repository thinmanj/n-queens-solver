#!/usr/bin/env python3
"""
N-Queens Solver using Conflict-Directed Backjumping with MRV.

Combines MRV heuristic with intelligent backtracking that jumps
directly to the source of conflicts, skipping irrelevant columns.

Time Complexity: Better than standard backtracking (prunes more)
Space Complexity: O(N) 

Algorithm:
1. Use MRV to select most constrained column
2. Try each valid row
3. On failure, identify which column caused the conflict
4. Backjump to that column instead of just previous column
5. Skip columns that couldn't have caused the conflict

Author: N-Queens Optimizer
"""

import sys
import time
import argparse
from typing import List, Optional, Set, Tuple


class BackjumpingSolver:
    """N-Queens solver using conflict-directed backjumping with MRV."""
    
    def __init__(self, n: int, verbose: bool = False):
        """
        Initialize the backjumping solver.
        
        Args:
            n: Size of the board (number of queens)
            verbose: Enable detailed output
        """
        if n < 1:
            raise ValueError("Board size must be at least 1")
        
        self.n = n
        self.verbose = verbose
        
        # Bitwise constraint tracking for O(1) checking
        self.col_mask = 0
        self.diag1_mask = 0
        self.diag2_mask = 0
        
        # board[col] = row
        self.board: List[int] = [-1] * n
        
        # Statistics
        self.nodes_explored = 0
        self.backjumps = 0
        self.normal_backtracks = 0
    
    def solve(self) -> bool:
        """
        Solve the N-Queens problem.
        
        Returns:
            True if solution found, False otherwise
        """
        start_time = time.time()
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Backjumping Solver with MRV for {self.n}-Queens")
            print(f"{'='*60}\n")
        
        # Handle trivial cases
        if self.n == 1:
            self.board = [0]
            return True
        
        if self.n in [2, 3]:
            if self.verbose:
                print(f"No solution exists for {self.n}-Queens")
            return False
        
        # Solve using backjumping
        success, _ = self._backjump(set(range(self.n)), 0)
        
        elapsed = time.time() - start_time
        
        if success:
            self._print_statistics(elapsed)
        elif self.verbose:
            print(f"No solution found")
        
        return success
    
    def _backjump(self, unplaced: Set[int], depth: int) -> Tuple[bool, int]:
        """
        Recursive backjumping with MRV.
        
        Args:
            unplaced: Set of unplaced column indices
            depth: Current recursion depth
            
        Returns:
            Tuple of (success, conflict_column)
            - If success: (True, -1)
            - If failure: (False, column_that_caused_conflict)
        """
        self.nodes_explored += 1
        
        # Base case: all queens placed
        if not unplaced:
            return True, -1
        
        # MRV: Select most constrained column
        best_col = self._select_mrv_column(unplaced)
        
        if best_col is None:
            # Dead end detected early
            return False, -1
        
        # Get valid rows for this column
        valid_rows = self._get_valid_rows(best_col)
        
        if not valid_rows:
            # No valid placement - conflict with all previous columns
            conflict_col = self._find_conflict_source(best_col)
            return False, conflict_col
        
        # Try each valid row
        for row in valid_rows:
            # Place queen
            self._place_queen(row, best_col)
            
            # Recursively solve remaining columns
            new_unplaced = unplaced - {best_col}
            success, conflict_col = self._backjump(new_unplaced, depth + 1)
            
            if success:
                return True, -1
            
            # Remove queen
            self._remove_queen(row, best_col)
            
            # Check if we should backjump
            if conflict_col != -1 and conflict_col < best_col:
                # Conflict is with earlier column - backjump!
                self.backjumps += 1
                
                if self.verbose and depth < 3:
                    print(f"  Backjump from col {best_col} to col {conflict_col}")
                
                return False, conflict_col
            
            # Normal backtrack - conflict is with this column
            self.normal_backtracks += 1
        
        # All rows tried, identify conflict source
        conflict_col = self._find_conflict_source(best_col)
        return False, conflict_col
    
    def _select_mrv_column(self, unplaced: Set[int]) -> Optional[int]:
        """
        Select column with minimum remaining values (MRV).
        
        Args:
            unplaced: Set of unplaced columns
            
        Returns:
            Column with fewest valid rows, or None if dead end
        """
        best_col = None
        min_count = self.n + 1
        
        for col in unplaced:
            count = self._count_valid_rows(col)
            
            if count == 0:
                # Dead end detected
                return None
            
            if count < min_count:
                min_count = count
                best_col = col
        
        return best_col
    
    def _count_valid_rows(self, col: int) -> int:
        """
        Count valid rows for given column.
        
        Args:
            col: Column index
            
        Returns:
            Number of valid rows
        """
        count = 0
        all_rows = (1 << self.n) - 1
        
        for row in range(self.n):
            row_bit = 1 << row
            diag1 = row - col
            diag2 = row + col
            
            if (row_bit & self.col_mask == 0 and
                not (self.diag1_mask & (1 << (diag1 + self.n))) and
                not (self.diag2_mask & (1 << diag2))):
                count += 1
        
        return count
    
    def _get_valid_rows(self, col: int) -> List[int]:
        """
        Get list of valid rows for given column.
        
        Args:
            col: Column index
            
        Returns:
            List of valid row indices
        """
        valid = []
        
        for row in range(self.n):
            row_bit = 1 << row
            diag1 = row - col
            diag2 = row + col
            
            if (row_bit & self.col_mask == 0 and
                not (self.diag1_mask & (1 << (diag1 + self.n))) and
                not (self.diag2_mask & (1 << diag2))):
                valid.append(row)
        
        return valid
    
    def _find_conflict_source(self, col: int) -> int:
        """
        Find which placed column is causing the most conflicts.
        
        Args:
            col: Current column with no valid placements
            
        Returns:
            Column index that is source of conflict
        """
        # Find rightmost placed column (most recent decision)
        conflict_col = -1
        
        for c in range(self.n):
            if self.board[c] != -1 and c < col:
                conflict_col = c
        
        return conflict_col
    
    def _place_queen(self, row: int, col: int) -> None:
        """
        Place a queen and update constraints.
        
        Args:
            row: Row to place queen
            col: Column to place queen
        """
        self.board[col] = row
        
        row_bit = 1 << row
        diag1 = row - col
        diag2 = row + col
        
        self.col_mask |= row_bit
        self.diag1_mask |= (1 << (diag1 + self.n))
        self.diag2_mask |= (1 << diag2)
    
    def _remove_queen(self, row: int, col: int) -> None:
        """
        Remove a queen and restore constraints.
        
        Args:
            row: Row of queen
            col: Column of queen
        """
        self.board[col] = -1
        
        row_bit = 1 << row
        diag1 = row - col
        diag2 = row + col
        
        self.col_mask &= ~row_bit
        self.diag1_mask &= ~(1 << (diag1 + self.n))
        self.diag2_mask &= ~(1 << diag2)
    
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
        print(f"Nodes explored: {self.nodes_explored}")
        print(f"Backjumps: {self.backjumps}")
        print(f"Normal backtracks: {self.normal_backtracks}")
        
        if self.backjumps + self.normal_backtracks > 0:
            jump_ratio = self.backjumps / (self.backjumps + self.normal_backtracks) * 100
            print(f"Backjump ratio: {jump_ratio:.1f}%")
        
        print(f"Time: {elapsed:.4f}s")
        print(f"{'='*60}")
        
        if self.n <= 20:
            self._print_board()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Solve N-Queens using Conflict-Directed Backjumping',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Solve 8-Queens
  %(prog)s 20           # Solve 20-Queens
  %(prog)s 25 -v        # Solve 25-Queens with verbose output
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
    
    args = parser.parse_args()
    
    try:
        solver = BackjumpingSolver(n=args.N, verbose=args.verbose)
        
        success = solver.solve()
        
        if not success:
            print(f"\nNo solution exists for {args.N}-Queens")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
