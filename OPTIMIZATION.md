# Optimization Results

## Performance Improvements

Optimized the N-Queens solver by replacing set-based constraint tracking with bitwise operations.

### Key Changes

1. **Bitwise Operations**: Replaced `set` operations with integer bitmasks
   - `cols` (set) → `col_mask` (int with bit flags)
   - `diag1` (set) → `diag1_mask` (int with bit flags)
   - `diag2` (set) → `diag2_mask` (int with bit flags)

2. **Memory Efficiency**: Reduced memory overhead
   - Sets require heap allocation per element
   - Integers use fixed-size stack memory

3. **Operation Speed**: Bitwise operations are CPU-native
   - `row in self.cols` → `self.col_mask & row_bit`
   - `self.cols.add(row)` → `self.col_mask |= row_bit`
   - `self.cols.remove(row)` → `self.col_mask ^= row_bit`

4. **Removed Instrumentation**: Eliminated `attempts` counter from hot path

### Benchmark Results (N=15)

| Version | Time | Improvement |
|---------|------|-------------|
| Set-based | 0.0151s | baseline |
| Bitwise | 0.0048s | **3.1x faster** |

### Performance Across Board Sizes

| N | Time (seconds) |
|---|----------------|
| 12 | 0.0009 |
| 15 | 0.0049 |
| 18 | 0.1625 |
| 20 | 1.0071 |

### Technical Details

**Diagonal Indexing:**
- Positive diagonals: `row - col + n - 1` (range: 0 to 2n-2)
- Negative diagonals: `row + col` (range: 0 to 2n-2)

**Bitwise Operations:**
- `|=` (OR): Set bit to 1 (add constraint)
- `^=` (XOR): Toggle bit to 0 (remove constraint)
- `&` (AND): Check if bit is 1 (test constraint)

### Why This Works

1. **O(1) Operations**: All bit operations are constant time
2. **Cache Friendly**: Integers fit in CPU registers
3. **No Allocations**: No dynamic memory allocation during solving
4. **Branch Prediction**: Simpler conditional logic

### Space Complexity

- **Before**: O(N) for board + O(N) average for 3 sets = O(N)
- **After**: O(N) for board + O(1) for 3 integers = O(N)
- Sets have per-element overhead (~24 bytes per entry in Python)
- Integers are fixed size (28 bytes for Python `int` object)

### Time Complexity

- **Worst case**: O(N!) - unchanged
- **Average case**: Significantly improved due to faster constraint checking
- **Best case**: O(N) - unchanged

## Conclusion

Bitwise optimization provides **3x speedup** with cleaner code and better memory efficiency.
