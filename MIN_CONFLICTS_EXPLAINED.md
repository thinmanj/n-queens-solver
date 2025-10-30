# Min-Conflicts Local Search Explained

## The Fundamental Difference

All previous algorithms (MRV, Backjumping, etc.) are **constructive search**:
- Start with empty board
- Add queens one by one
- Backtrack when stuck

Min-Conflicts is **local search**:
- Start with ALL queens placed (complete assignment)
- Iteratively FIX conflicts
- Move queens to better positions

## The Hill Climbing Analogy

Imagine you're blindfolded on a mountain, trying to find the peak:

### Constructive Search (MRV, Backjumping)
```
Start at bottom:
 ↓
 ·  ·  ·  /\  ← Peak (solution)
 ·  ·  /    \
 ·  /        \
[·] ← You start here, climb step by step

Problem: If you hit a cliff, must go ALL THE WAY BACK DOWN
```

### Local Search (Min-Conflicts)
```
Start anywhere:
          /\  ← Peak (solution)
    [·]  /  \  ← You start here randomly
   /  \ /    \
  /    ·      \

Problem: Might get stuck in local peak
Solution: Restart from random position if stuck
```

## Visual Example: 4-Queens

### Step 0: Random Initial Placement
```
   0 1 2 3
0  Q Q Q Q  ← All queens placed randomly!
1  · · · ·
2  · · · ·
3  · · · ·

Conflicts:
- Row 0: ALL FOUR queens attacking each other
- Total conflicts: 6 (each pair = 1 conflict)
```

### Step 1: Pick Column with Conflicts
```
Pick col 1 (has conflicts):
   0 1 2 3
0  Q[Q]Q Q  ← This queen has 3 conflicts
1  · · · ·
2  · · · ·
3  · · · ·
```

### Step 2: Find Best Row for Col 1
```
Try each row, count conflicts:

Row 0: [Q]Q Q Q  → 3 conflicts (stays same)
Row 1:  Q · Q Q  → 2 conflicts (better!)
Row 2:  Q · Q Q  → 2 conflicts (better!)
Row 3:  Q · Q Q  → 2 conflicts (better!)

Choose row 1 (random among ties):
   0 1 2 3
0  Q · Q Q
1  ·[Q]· ·  ← Moved here!
2  · · · ·
3  · · · ·

New total conflicts: 3 (improved!)
```

### Step 3: Pick Another Conflicted Column
```
Pick col 2 (has conflicts):
   0 1 2 3
0  Q ·[Q]Q  ← This queen has 2 conflicts
1  · Q · ·
2  · · · ·
3  · · · ·

Try each row:
Row 0: Q · Q Q  → 2 conflicts
Row 1: Q · Q Q  → 1 conflict (col 1 diagonal)
Row 2: Q · Q Q  → 2 conflicts
Row 3: Q · Q Q  → 1 conflict (col 3 diagonal)

Choose row 3:
   0 1 2 3
0  Q · · Q
1  · Q · ·
2  · · · ·
3  · ·[Q]·  ← Moved here!

New total conflicts: 2
```

### Step 4: Continue Until No Conflicts
```
Pick col 0:
Try each row... row 2 has 0 conflicts!
   0 1 2 3
0  · · · Q
1  · Q · ·
2 [Q]· · ·  ← Moved here!
3  · · Q ·

Pick col 3:
Try each row... row 1 has 0 conflicts!
   0 1 2 3
0  · · · ·
1  · Q ·[Q] ← Moved here!
2  Q · · ·
3  · · Q ·

SOLUTION FOUND! Zero conflicts! ✓
```

## The Algorithm Step-by-Step

### 1. Random Initialization
```python
# Place one queen per column at random row
board = [random.randint(0, n-1) for col in range(n)]

Example N=8:
board = [3, 7, 1, 4, 2, 0, 6, 5]
        ↑              ↑
      col 0          col 7
   (row 3)        (row 5)
```

### 2. Find Conflicted Columns
```python
conflicted_cols = []
for col in range(n):
    if count_conflicts(col) > 0:
        conflicted_cols.append(col)

Example:
conflicted_cols = [0, 2, 3, 5, 7]  # 5 columns have conflicts
```

### 3. Pick Random Conflicted Column
```python
col = random.choice(conflicted_cols)
```
**Why random?** Helps escape local minima

### 4. Find Min-Conflict Row
```python
min_conflicts = n
best_rows = []

for row in range(n):
    board[col] = row  # Try this row
    conflicts = count_conflicts(col)
    
    if conflicts < min_conflicts:
        min_conflicts = conflicts
        best_rows = [row]
    elif conflicts == min_conflicts:
        best_rows.append(row)

# Pick random among ties
board[col] = random.choice(best_rows)
```

### 5. Repeat Until Solved
```python
for step in range(max_steps):
    conflicted_cols = find_conflicted_columns()
    
    if not conflicted_cols:
        return True  # SOLUTION!
    
    col = random.choice(conflicted_cols)
    board[col] = find_min_conflict_row(col)

# If max_steps reached without solution: RESTART
```

## Why It's Fast for Large N

### Traditional Backtracking (N=1000)
```
Search space: Astronomically large
Nodes to explore: 1000^1000 (impossible!)
Time: Would take millions of years

Board states explored:
Empty → 1 queen → 2 queens → ... → 1000 queens
         ↓ backtrack ↓ backtrack ... endless
```

### Min-Conflicts (N=1000)
```
Search space: Only 1000 positions per queen
Typical steps to solution: ~700 steps
Time: 175 seconds ✓

Board states explored:
Random complete → Move 1 queen → Move 1 queen → ...
                    ↓              ↓
                Better          Better        SOLUTION!
```

## The Landscape Metaphor

### Complete Search (MRV/Backjumping)
```
Solution space as a tree:

                   ○ Solution
                  /|\
                 / | \
                /  |  \
         Dead ends (must backtrack)
           /|\  /|\  /|\
          
Must explore systematically
Can't skip branches without proof
```

### Local Search (Min-Conflicts)
```
Solution space as a landscape:

    Peak         Peak        Valley  Peak (Solution!)
     /\           /\          /  \      /\
    /  \         /  \        /    \    /  \
   /    \       /    \      /      \  /    \
  
Can jump around randomly
Can get stuck in local peaks (restart!)
```

## Real Example: N=50

### Standard Backtracking
```
Time: 0.1449s
Nodes explored: 756
Strategy: Systematic construction
Result: ✓ Solution guaranteed
```

### Min-Conflicts
```
Time: 0.0320s (4.5x FASTER!)
Nodes explored: 49 (just moved each queen once!)
Strategy: Random improvement
Result: ✓ Solution found (not guaranteed)
```

**Why so much faster?**
- Didn't explore dead ends
- Each step makes progress toward solution
- No backtracking overhead

## The Conflict Counting

### How to Count Conflicts for a Queen
```python
def count_conflicts(col):
    row = board[col]
    conflicts = 0
    
    for other_col in range(n):
        if other_col == col:
            continue
        
        other_row = board[other_col]
        
        # Same row?
        if other_row == row:
            conflicts += 1
        
        # Same diagonal?
        elif abs(other_row - row) == abs(other_col - col):
            conflicts += 1
    
    return conflicts
```

### Visual: Conflict Counting
```
   0 1 2 3 4 5
0  · · Q · · ·  ← Conflict! Same row
1  · · · · · ·
2  Q · · · · ·  ← No conflict
3  · · · ·[Q]·  ← This queen (checking conflicts)
4  · · · · · Q  ← Conflict! Same diagonal (slope -1)
5  · Q · · · ·  ← No conflict

Total conflicts for col 4: 2
```

## When Min-Conflicts Gets Stuck

### Local Minimum Example
```
   0 1 2 3
0  Q · · ·
1  · · Q ·
2  · · · Q
3  · Q · ·

Conflicts: 2 (cols 1-2, cols 2-3 on diagonals)

But moving any single queen makes it WORSE:
- Move col 1: Creates 3+ conflicts
- Move col 2: Creates 3+ conflicts

This is a LOCAL MINIMUM (not a solution!)
```

**Solution**: RESTART from new random configuration
```python
max_steps_per_restart = n * n
max_restarts = 100

for restart in range(max_restarts):
    board = random_configuration()
    
    if min_conflicts_search(board, max_steps_per_restart):
        return True  # Found solution!

return False  # Failed after all restarts
```

## Performance Characteristics

### Completeness
- ❌ **Not complete**: Might fail to find solution
- ⚠️ **Probabilistically complete**: Almost always finds solution with restarts
- ✅ **Practical**: Fails rarely for N-Queens

### Time Complexity
- **Best case**: O(N) - Each queen moves once
- **Average case**: O(N) to O(N²) - Few restarts needed
- **Worst case**: O(∞) - Might never find solution (restart limit prevents this)

### Space Complexity
- O(N) - Just stores board array
- Much less than backtracking (no recursion stack)

## Benchmark Results

| N | Time | Steps | Restarts | Success Rate |
|---|------|-------|----------|--------------|
| 8 | 0.0003s | 12 | 1 | 100% |
| 50 | 0.0320s | 49 | 1 | 100% |
| 100 | 0.4066s | 180 | 1 | 100% |
| 1000 | 175.8s | 700 | 1 | 100% |

**Key insight**: Steps scales sub-linearly with N!

## Comparison: Complete vs Local Search

### Complete Search (MRV, Backjumping)
✅ **Guaranteed** to find solution if one exists  
✅ **Systematic** exploration  
✅ **Predictable** performance  
❌ **Doesn't scale** to large N (>100)  
❌ **Explores dead ends**

### Local Search (Min-Conflicts)
❌ **Not guaranteed** (but almost always succeeds)  
✅ **Scales** to N=1000+  
✅ **Simple** implementation  
⚠️ **Variable** performance (randomized)  
✅ **No dead end exploration**

## The Restaurant Seating Analogy

### Complete Search
```
Seat guests one by one:
- Guest 1: Any seat (100 choices)
- Guest 2: Compatible with guest 1 (70 choices)
- Guest 3: Compatible with guests 1,2 (40 choices)
- ...
- Guest 50: No valid seat!
- Remove guest 49, try again
- Remove guest 48, try again
- ...endless backtracking

Like planning a seating chart perfectly before anyone sits down
```

### Local Search
```
Seat all guests randomly:
- Some conflicts (people who don't get along sitting together)
- Move ONE person to a better seat
- Move ANOTHER person to a better seat
- ...
- After 50 moves, everyone is happy!

Like letting everyone sit randomly, then asking unhappy people to move
```

## Key Takeaways

1. **Different Paradigm**: Complete assignment + improvement (not construction)
2. **Trade-off**: Completeness for scalability
3. **Randomization**: Essential for escaping local minima
4. **Restarts**: Cheap way to avoid getting stuck
5. **Scales Amazingly**: O(N) typical steps vs O(N!) backtracking

## When to Use Min-Conflicts

### ✅ Use Min-Conflicts When:
- N > 50 (where complete algorithms struggle)
- You can tolerate restarts
- You need speed over guarantees
- Exploring all possibilities is impossible

### ❌ Use Complete Search When:
- You need guaranteed solution
- N ≤ 50 (where complete is fast enough)
- You need to prove unsolvability
- Deterministic behavior required

## Code Structure

```python
class MinConflictsSolver:
    def solve(self):
        for restart in range(max_restarts):
            self._random_initialization()
            
            if self._min_conflicts_search():
                return True  # Success!
        
        return False  # Failed
    
    def _min_conflicts_search(self):
        for step in range(max_steps):
            # Find conflicted columns
            conflicted = self._get_conflicted_columns()
            
            if not conflicted:
                return True  # SOLUTION!
            
            # Pick random conflicted column
            col = random.choice(conflicted)
            
            # Move to min-conflict row
            self.board[col] = self._min_conflict_row(col)
        
        return False  # Exceeded max steps
```

Simple, elegant, and scales to N=1000+!

## Combining with Other Techniques

### Min-Conflicts + Simulated Annealing
```python
# Accept worse moves sometimes (escape local minima)
if new_conflicts <= current_conflicts or random() < temperature:
    accept_move()
```

### Min-Conflicts + Tabu Search
```python
# Remember recent moves, don't repeat them
if (col, row) not in tabu_list:
    make_move(col, row)
```

### Min-Conflicts + Parallel Search
```python
# Run multiple searches simultaneously
results = parallel_map(min_conflicts_solve, random_seeds)
return first_success(results)
```

## Final Thoughts

Min-Conflicts shows that sometimes:
- **Working backwards** (from complete to correct) beats working forwards
- **Approximation** (local search) beats exact search
- **Simplicity** (random improvement) beats complexity

It's not always the "smartest" algorithm, but for large N, it's the only practical one!
