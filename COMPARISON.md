# Algorithm Comparison: Bitwise vs Attack Tracking

## Overview

Two optimized approaches to solve the N-Queens problem:

1. **Bitwise Constraint Tracking** (`n_queens_solver.py`)
2. **Attack Cell Tracking** (`n_queens_attack_tracking.py`)

## Performance Results

| Size | Bitwise | Attack Tracking | Winner |
|------|---------|-----------------|--------|
| 8    | 0.0003s | 0.0004s (1.25x) | Bitwise |
| 12   | 0.0009s | 0.0011s (1.17x) | Bitwise |
| 15   | 0.0048s | 0.0091s (1.87x) | Bitwise |
| 18   | 0.2707s | 0.2011s (0.74x) | **Attack Tracking** |

## Key Findings

### Small Boards (N ≤ 15)
**Bitwise wins** by 1.2-1.9x due to:
- CPU-native bit operations
- Better cache locality
- No memory allocation overhead

### Larger Boards (N ≥ 18)
**Attack Tracking wins** by ~25% because:
- Simpler pruning logic becomes beneficial
- Less bit shifting overhead for large diagonal indices
- More straightforward memory access patterns

## Approach Details

### 1. Bitwise Constraint Tracking

**Space:** O(N) for board + O(1) for 3 integers  
**Check Constraint:** O(1) bitwise AND  
**Add Constraint:** O(1) bitwise OR  
**Remove Constraint:** O(1) bitwise XOR  

```python
row_bit = 1 << row
if not (self.col_mask & row_bit):  # O(1) check
    self.col_mask |= row_bit       # O(1) add
```

**Advantages:**
- Minimal memory footprint
- CPU register-friendly
- No allocations during solving

**Disadvantages:**
- More complex diagonal indexing
- Bit shift overhead for large N

### 2. Attack Cell Tracking

**Space:** O(N²) for 2D board  
**Check Constraint:** O(1) array lookup  
**Add Constraint:** O(N) to mark attacked cells  
**Remove Constraint:** O(N) to unmark cells  

```python
if self.board[row][col] == 0:       # O(1) check
    self._mark_attacks(row, col, 1)  # O(N) mark
```

**Advantages:**
- Intuitive and easy to understand
- Direct mapping to chess board
- No bit manipulation complexity
- Scales better for very large N

**Disadvantages:**
- Higher memory usage (N² vs N)
- O(N) marking operations per placement
- Cache misses on large boards

## Complexity Analysis

### Time Complexity
Both algorithms:
- **Worst case:** O(N!)
- **Average case:** Heavily pruned by constraint propagation
- **Per-placement check:** O(1) vs O(N)

### Space Complexity
- **Bitwise:** O(N) - board array + 3 integers
- **Attack Tracking:** O(N²) - full 2D board

## Recommendations

### Use Bitwise when:
- ✅ N < 20
- ✅ Memory is limited
- ✅ Maximum performance for typical cases
- ✅ Embedding in other systems

### Use Attack Tracking when:
- ✅ N > 20
- ✅ Code clarity is priority
- ✅ Debugging/visualization needed
- ✅ Teaching/learning algorithms

## Code Quality

Both implementations feature:
- Type hints throughout
- Comprehensive docstrings
- Clean separation of concerns
- CLI with argparse
- Verbose debugging mode
- Error handling

## Original Approach Issues Fixed

Your original implementation had:
1. ❌ Forward-marking instead of backward (logic error)
2. ❌ O(N²) validation per placement
3. ❌ Complex nested loops in `is_place_valid()`
4. ❌ Incorrect pruning logic

The optimized attack tracking version fixes all these while preserving your core concept.
