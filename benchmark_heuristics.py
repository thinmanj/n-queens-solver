#!/usr/bin/env python3
"""
Benchmark script for comparing N-Queens solver implementations.

Tests various algorithms across different N values and generates
comprehensive performance comparison data.

Author: N-Queens Optimizer
"""

import sys
import time
import importlib
import argparse
from typing import Dict, List, Tuple, Optional


class BenchmarkRunner:
    """Runs benchmarks on different N-Queens solvers."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize benchmark runner.
        
        Args:
            verbose: Enable detailed output
        """
        self.verbose = verbose
        self.results: Dict[str, Dict[int, Dict[str, any]]] = {}
    
    def benchmark_solver(self, solver_name: str, n: int, timeout: float = 30.0) -> Optional[Dict[str, any]]:
        """
        Benchmark a specific solver on given N.
        
        Args:
            solver_name: Name of solver module
            n: Board size
            timeout: Maximum time to allow (seconds)
            
        Returns:
            Dictionary with timing and statistics, or None if failed/timeout
        """
        try:
            # Import solver module
            module = importlib.import_module(solver_name)
            
            # Create solver instance based on module type
            if solver_name == 'n_queens_min_conflicts':
                solver = module.MinConflictsSolver(n=n, verbose=False, max_restarts=100)
            elif solver_name == 'n_queens_backjumping':
                solver = module.BackjumpingSolver(n=n, verbose=False)
            elif solver_name == 'n_queens_heuristic':
                solver = module.NQueensMRV(n=n, verbose=False)
            else:
                # Generic solver
                solver = module.NQueensSolver(n=n, verbose=False)
            
            # Time the solve
            start_time = time.time()
            success = solver.solve()
            elapsed = time.time() - start_time
            
            if not success or elapsed > timeout:
                return None
            
            # Collect statistics
            result = {
                'time': elapsed,
                'nodes': getattr(solver, 'nodes_explored', 0),
                'success': success
            }
            
            # Add solver-specific stats
            if hasattr(solver, 'backjumps'):
                result['backjumps'] = solver.backjumps
                result['normal_backtracks'] = solver.normal_backtracks
            
            if hasattr(solver, 'restarts_used'):
                result['restarts'] = solver.restarts_used
                result['total_steps'] = solver.total_steps
            
            return result
            
        except Exception as e:
            if self.verbose:
                print(f"  Error benchmarking {solver_name} with N={n}: {e}")
            return None
    
    def run_benchmarks(self, test_sizes: List[int]) -> None:
        """
        Run benchmarks on all solvers for given N values.
        
        Args:
            test_sizes: List of N values to test
        """
        # Solvers to benchmark
        solvers = [
            ('n_queens_heuristic', 'MRV'),
            ('n_queens_backjumping', 'Backjumping'),
            ('n_queens_min_conflicts', 'Min-Conflicts'),
        ]
        
        print(f"\n{'='*70}")
        print(f"Benchmarking N-Queens Solvers")
        print(f"{'='*70}\n")
        
        for n in test_sizes:
            print(f"Testing N={n}...")
            
            for module_name, display_name in solvers:
                if self.verbose:
                    print(f"  Running {display_name}...")
                
                result = self.benchmark_solver(module_name, n, timeout=30.0)
                
                if result:
                    if display_name not in self.results:
                        self.results[display_name] = {}
                    self.results[display_name][n] = result
                    
                    if self.verbose:
                        print(f"    Time: {result['time']:.4f}s, Nodes: {result['nodes']}")
                else:
                    if self.verbose:
                        print(f"    Failed or timeout")
            
            print()
    
    def print_results(self) -> None:
        """Print benchmark results in table format."""
        print(f"\n{'='*70}")
        print(f"Benchmark Results")
        print(f"{'='*70}\n")
        
        # Get all N values tested
        all_n_values = set()
        for solver_results in self.results.values():
            all_n_values.update(solver_results.keys())
        all_n_values = sorted(all_n_values)
        
        # Print header
        print(f"{'Solver':<20} ", end='')
        for n in all_n_values:
            print(f"N={n:<6} ", end='')
        print()
        print('-' * 70)
        
        # Print results for each solver
        for solver_name in sorted(self.results.keys()):
            print(f"{solver_name:<20} ", end='')
            
            for n in all_n_values:
                if n in self.results[solver_name]:
                    time_val = self.results[solver_name][n]['time']
                    print(f"{time_val:>8.4f}s ", end='')
                else:
                    print(f"{'FAIL':>9} ", end='')
            
            print()
        
        print()
    
    def print_detailed_comparison(self, n: int) -> None:
        """
        Print detailed comparison for specific N.
        
        Args:
            n: Board size to compare
        """
        print(f"\n{'='*70}")
        print(f"Detailed Comparison for N={n}")
        print(f"{'='*70}\n")
        
        # Find fastest solver
        fastest_time = float('inf')
        fastest_solver = None
        
        for solver_name, results in self.results.items():
            if n in results:
                time_val = results[n]['time']
                if time_val < fastest_time:
                    fastest_time = time_val
                    fastest_solver = solver_name
        
        # Print comparison
        for solver_name in sorted(self.results.keys()):
            if n not in self.results[solver_name]:
                continue
            
            result = self.results[solver_name][n]
            time_val = result['time']
            nodes = result['nodes']
            
            speedup = fastest_time / time_val if time_val > 0 else 1.0
            
            print(f"{solver_name}:")
            print(f"  Time: {time_val:.4f}s")
            print(f"  Nodes explored: {nodes:,}")
            print(f"  Speedup vs fastest: {speedup:.2f}x")
            
            # Solver-specific stats
            if 'backjumps' in result:
                print(f"  Backjumps: {result['backjumps']}")
                print(f"  Normal backtracks: {result['normal_backtracks']}")
            
            if 'restarts' in result:
                print(f"  Restarts: {result['restarts']}")
                print(f"  Total steps: {result['total_steps']}")
            
            print()
    
    def generate_markdown_table(self) -> str:
        """
        Generate markdown table of results.
        
        Returns:
            Markdown formatted table
        """
        all_n_values = set()
        for solver_results in self.results.values():
            all_n_values.update(solver_results.keys())
        all_n_values = sorted(all_n_values)
        
        lines = []
        lines.append("\n## Performance Comparison Table\n")
        
        # Header
        header = "| Solver |"
        separator = "|--------|"
        for n in all_n_values:
            header += f" N={n} |"
            separator += "------|"
        
        lines.append(header)
        lines.append(separator)
        
        # Data rows
        for solver_name in sorted(self.results.keys()):
            row = f"| **{solver_name}** |"
            
            for n in all_n_values:
                if n in self.results[solver_name]:
                    time_val = self.results[solver_name][n]['time']
                    row += f" {time_val:.4f}s |"
                else:
                    row += " - |"
            
            lines.append(row)
        
        return '\n'.join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Benchmark N-Queens solver implementations',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--sizes',
        type=str,
        default='8,10,12,15,20,25',
        help='Comma-separated list of N values to test (default: 8,10,12,15,20,25)'
    )
    
    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Output results as markdown table'
    )
    
    args = parser.parse_args()
    
    # Parse test sizes
    try:
        test_sizes = [int(x.strip()) for x in args.sizes.split(',')]
    except ValueError:
        print("Error: Invalid sizes format. Use comma-separated integers.", file=sys.stderr)
        sys.exit(1)
    
    # Run benchmarks
    runner = BenchmarkRunner(verbose=args.verbose)
    
    try:
        runner.run_benchmarks(test_sizes)
        runner.print_results()
        
        # Print detailed comparison for a few key sizes
        if 20 in test_sizes:
            runner.print_detailed_comparison(20)
        
        if args.markdown:
            print(runner.generate_markdown_table())
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
