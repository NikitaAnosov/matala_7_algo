from typing import Dict, List, Tuple, Any
import math


def max_mean_cycle(
        graph: Dict[Any, List[Tuple[Any, float]]]
) -> Tuple[List[Any], float]:
    """
    Finds a cycle of maximum average weight in a directed graph using
    Karp's algorithm.

    Parameters:
    -----------
    graph : dict
        A mapping from each vertex v to a list of (neighbor, weight) edges.

    Returns:
    --------
    cycle : list
        A list of vertices [v0, v1, ..., vk = v0] representing the cycle
        with maximum mean weight.
    mean_weight : float
        The average weight of that cycle.

    Runtime is O(n * m), where n = |V| and m = |E|.
    """
    # 1. Indexing
    nodes = list(graph.keys())
    n = len(nodes)
    idx = {v: i for i, v in enumerate(nodes)}

    # 2. Build reverse adjacency for predecessors
    rev = {v: [] for v in nodes}
    for u, nbrs in graph.items():
        for v, w in nbrs:
            rev[v].append((u, w))

    # 3. DP tables: dp[k][i] = max weight of any path of length k ending at nodes[i]
    dp = [[-math.inf] * n for _ in range(n + 1)]
    pred = [[None] * n for _ in range(n + 1)]
    # base case: path of length 0 has weight 0 at every node
    for i in range(n):
        dp[0][i] = 0.0

    # 4. Fill DP
    for k in range(1, n + 1):
        for v in nodes:
            j = idx[v]
            best = -math.inf
            best_u = None
            for u, w in rev[v]:
                i = idx[u]
                val = dp[k - 1][i] + w
                if val > best:
                    best = val
                    best_u = u
            dp[k][j] = best
            pred[k][j] = best_u

    # 5. Compute for each v: mu[v] = min_{0 <= k < n} (dp[n][v] - dp[k][v]) / (n - k)
    mu = [-math.inf] * n
    argmin_k = [0] * n
    for v in nodes:
        j = idx[v]
        best_val = math.inf
        best_k = 0
        for k in range(n):
            if dp[k][j] > -math.inf:
                val = (dp[n][j] - dp[k][j]) / (n - k)
                if val < best_val:
                    best_val = val
                    best_k = k
        mu[j] = best_val
        argmin_k[j] = best_k

    # 6. Pick the vertex v* with maximum mu[v]
    j_star = max(range(n), key=lambda j: mu[j])
    mean_weight = mu[j_star]
    k_star = argmin_k[j_star]
    v_star = nodes[j_star]

    # 7. Reconstruct a walk of length n ending at v_star
    walk = [v_star]
    cur = v_star
    for k in range(n, 0, -1):
        u = pred[k][idx[cur]]
        walk.append(u)
        cur = u
    walk.reverse()  # now walk[0] → ... → walk[n] = v_star

    # 8. Extract the subwalk from position k_star to n, then find a simple cycle
    subwalk = walk[k_star:]
    seen = {}
    cycle = []
    for i, v in enumerate(subwalk):
        if v in seen:
            start = seen[v]
            cycle = subwalk[start: i + 1]
            break
        seen[v] = i

    return cycle, mean_weight


# Example usage and simple test
if __name__ == "__main__":
    # graph as adjacency list: node -> list of (neighbor, weight)
    G1 = {
        'A': [('B', 3), ('C', 2)],
        'B': [('C', 1), ('A', -4)],
        'C': [('A', 2)]
    }
    cycle, mean_w = max_mean_cycle(G1)
    print("Max-mean cycle:", cycle)
    print("Average weight:", mean_w)
    # Expected cycle: ['C', 'A', 'C'] with mean weight 2.0

    G2 = {
        'X': [('Y', 10)],
        'Y': [('X', -5)]
    }
    cycle2, mean2 = max_mean_cycle(G2)
    print("Max-mean cycle:", cycle2)
    print("Average weight:", mean2)
    # Expected cycle: ['X', 'Y', 'X'] with average (10 + (-5)) / 2 = 2.5

    G3 = {
        'D': [('D', 7)],
        'E': [('D', 1)]
    }
    cycle3, mean3 = max_mean_cycle(G3)
    print("Max-mean cycle:", cycle3)
    print("Average weight:", mean3)
    # Expected cycle: ['D', 'D'] with average 7.0

    G4 = {
        1: [(2, 5), (3, 2)],
        2: [(3, 4), (4, 1)],
        3: [(1, -2), (4, 3)],
        4: [(2, -1)]
    }
    cycle4, mean4 = max_mean_cycle(G4)
    print("Max-mean cycle:", cycle4)
    print("Average weight:", mean4)
    # Observed max-mean cycle: [2, 3, 1, 2] with average (4 + (-2) + 5) / 3 ≈ 2.3333