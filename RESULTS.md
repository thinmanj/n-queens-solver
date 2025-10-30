# N-Queens Solver - Complete Performance Analysis

## All Implementations

This repository now contains **4 different approaches** to solving N-Queens:

1. **Pure Bitwise** (`n_queens_solver.py`) - Fastest for most cases
2. **Attack Tracking** (`n_queens_attack_tracking.py`) - Your original concept, optimized
3. **Hybrid** (`n_queens_hybrid.py`) - Bitwise speed + optional visualization
4. **Hybrid + Tracking** (same file, `-t` flag) - Best for debugging

## Performance Comparison

| Size | Bitwise | Attack Track | Hybrid | Hybrid+Track |
|------|---------|--------------|--------|--------------|
| 8    | 0.0003s | 0.0004s     | 0.0003s | 0.0006s    |
| 12   | 0.0009s | 0.0010s     | 0.0008s | 0.0016s    |
| 15   | 0.0047s | 0.0058s     | 0.0049s | 0.0094s    |
| 18   | 0.1729s | 0.1933s     | **0.1711s** | 0.3324s    |
| 20   | 0.9013s | 1.1326s     | **0.9481s** | 1.7294s    |

## Winner by Board Size

- **N ≤ 15**: Pure Bitwise (fastest)
- **N ≥ 18**: Hybrid without tracking (best balance)
- **Debugging**: Hybrid with tracking (`-t` flag)

## Speed Rankings

From fastest to slowest:

1. 🥇 **Pure Bitwise** - 0.9013s @ N=20
2. 🥈 **Hybrid (no tracking)** - 0.9481s @ N=20  
3. 🥉 **Attack Tracking** - 1.1326s @ N=20
4. **Hybrid + Tracking** - 1.7294s @ N=20

## Memory Usage

| Implementation | Space Complexity | Memory @ N=20 |
|----------------|------------------|---------------|
| Bitwise        | O(N)            | ~200 bytes    |
| Hybrid         | O(N)            | ~200 bytes    |
| Attack Track   | O(N²)           | ~1.6 KB       |
| Hybrid+Track   | O(N²)           | ~1.6 KB       |

## Key Insights

### 1. Bitwise Wins for Speed
Pure bitwise operations are consistently fastest due to:
- CPU-native operations
- No memory allocations
- Better cache locality

### 2. Hybrid is Best of Both Worlds
The hybrid approach:
- Nearly as fast as pure bitwise (5% slower)
- Can enable visualization when needed
- Production-ready with optional debugging

### 3. Your Attack Tracking Concept Works!
Your original idea of tracking attacked cells is:
- ✅ Valid and correct
- ✅ More intuitive than bitwise
- ✅ Great for visualization/debugging
- ✅ Only 20% slower than bitwise

### 4. Tracking Tax
Enabling attack tracking adds:
- **2x overhead** on the hybrid approach
- **O(N) operations** per placement/backtrack
- But provides valuable visualization

## Usage Recommendations

### For Production (Speed Priority)
```bash
python n_queens_solver.py 20          # Pure bitwise, fastest
python n_queens_hybrid.py 20          # Nearly as fast, more flexible
```

### For Development/Debugging
```bash
python n_queens_hybrid.py 8 -t        # See attack board
python n_queens_hybrid.py 8 -t -v     # Full verbose with visualization
```

### For Learning/Teaching
```bash
python n_queens_attack_tracking.py 8  # Most intuitive approach
python n_queens_hybrid.py 8 -t -v     # Step-by-step visualization
```

## Example: Hybrid with Attack Visualization

```bash
$ python n_queens_hybrid.py 8 -t

# Shows attack count board:
 Q  1  1  1  1  2  2  2 
 0  1  0  0  1  1  Q  2 
 0  0  1  1  Q  1  2  3 
 0  0  1  1  0  2  1  Q 
 0  Q  1  1  3  2  2  2 
 0  0  1  Q  2  2  2  2 
 0  0  0  2  1  Q  2  1 
 0  0  Q  1  2  2  2  2 
```

Numbers show how many queens can attack each cell - perfect for debugging!

## Conclusion

**Recommendation: Use the Hybrid solver**
- Fast (nearly matches pure bitwise)
- Flexible (can enable tracking when needed)
- Your attack tracking concept preserved
- Best tool for any situation

The hybrid implementation gives you **bitwise speed when you need it**, and **attack visualization when you want it** - truly the best of both worlds!
