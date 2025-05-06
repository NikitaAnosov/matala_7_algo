# Maximum Mean Cycle Finder

This repository includes an implementation of **Karp's algorithm** for finding a cycle with maximum average weight in a directed graph. The main function is:

```python
max_mean_cycle(graph: Dict[Any, List[Tuple[Any, float]]]) -> Tuple[List[Any], float]
```
---

## 1. Algorithm Overview

1. **Indexing vertices**: We assign each vertex a unique integer index to work with arrays instead of arbitrary keys.
2. **Reverse adjacency**: For each vertex `v`, we collect all incoming edges `(u -> v)` with their weights.
3. **Dynamic programming table**:

   * We build a table `dp[k][i]` that stores the maximum total weight of any walk of exactly length `k` ending at vertex `i`.
   * Base case: `dp[0][i] = 0` for all `i`, since a path of length 0 has zero weight.
4. **Filling the table**:

   * For each `k` from 1 to `n` (number of vertices), and for each vertex `v`, we look at every predecessor `u` of `v`. We update

     ```
     dp[k][v] = max(dp[k-1][u] + weight(u->v))
     ```
     
5. **Computing mean weights**:

   * For each vertex `v`, consider all path lengths `k < n`. Compute the average weight gained per edge if you extend a walk of length `k` to length `n`.

   * Intuition: this finds the smallest “drop” in average if you compare shorter prefix to the full-length walk.  Karp’s theorem shows that the largest of these minima (over all `v`) equals the maximum cycle mean.
     
6. **Selecting the best vertex**.

7. **Reconstructing a cycle**:

   * Rebuild a walk of length `n` ending at `v*` by following the `pred` pointers backward.
   * From that length-`n` walk, extract the sub-walk from position `k*` to `n`.  Inside, find the first repeated vertex to isolate a simple cycle.
     
8. **Return** the cycle found and its average weight.

This approach runs in $O(n \times m)$ time, where $n$ is the number of vertices and $m$ is the number of edges.

---

## 2. Examples

**Example 1**:
```
G1 = {
    'A': [('B', 3), ('C', 2)],
    'B': [('C', 1), ('A', -4)],
    'C': [('A', 2)]
}
cycle1, mean1 = max_mean_cycle(G1)
```
- Observed cycle: ['C', 'A', 'C'] with mean weight 2.0

**Example 2**:
```
G2 = {
    'X': [('Y', 10)],
    'Y': [('X', -5)]
}
cycle2, mean2 = max_mean_cycle(G2)
```
- Observed cycle: ['X', 'Y', 'X'] with mean weight (10 + (-5)) / 2 = 2.5

**Example 3**:
```
G3 = {
    'D': [('D', 7)],
    'E': [('D', 1)]
}
cycle3, mean3 = max_mean_cycle(G3)
```
- Observed cycle: ['D', 'D'] with mean weight 7.0

**Example 4**:
```
G4 = {
    1: [(2, 5), (3, 2)],
    2: [(3, 4), (4, 1)],
    3: [(1, -2), (4, 3)],
    4: [(2, -1)]
}
cycle4, mean4 = max_mean_cycle(G4)
```
- Observed max-mean cycle: [2, 3, 1, 2] with average (4 + (-2) + 5) / 3 ≈ 2.3333


## 6. References

* Karp, R. M. (1978). A characterization of the minimum cycle mean in a digraph. *Discrete Mathematics, 23*(3), 309–311.

---

## 7. Credits
ChatGPT o4_mini_high for helping build the algorithm.

[Link](https://chatgpt.com/share/681a0ec4-894c-800b-8c48-3b928ae67361)

