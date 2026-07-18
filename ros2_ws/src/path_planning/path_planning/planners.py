#!/usr/bin/env python3
from __future__ import annotations

import heapq

import numpy as np


# ── line-of-sight check (shared) ────────────────────────────────────────────
def _segment_free(grid, a_world, b_world):
    """True if the straight segment a->b passes only through free voxels."""
    a = np.asarray(a_world, float)
    b = np.asarray(b_world, float)
    dist = np.linalg.norm(b - a)
    n = max(2, int(np.ceil(dist / (grid.res * 0.5))))  # sample at ~half-voxel
    for t in np.linspace(0.0, 1.0, n):
        p = a + t * (b - a)
        if not grid.is_free(grid.world_to_grid(p)):
            return False
    return True


def shortcut(grid, path):
    """Greedy line-of-sight shortcutting: drop waypoints we can skip."""
    if path is None or len(path) < 3:
        return path
    out = [path[0]]
    i = 0
    while i < len(path) - 1:
        j = len(path) - 1
        while j > i + 1 and not _segment_free(grid, path[i], path[j]):
            j -= 1
        out.append(path[j])
        i = j
    return out


# ── A* on the voxel grid ────────────────────────────────────────────────────
_NEIGHBORS = [
    (di, dj, dk)
    for di in (-1, 0, 1)
    for dj in (-1, 0, 1)
    for dk in (-1, 0, 1)
    if not (di == 0 and dj == 0 and dk == 0)
]


def _no_corner_cut(grid, ci, cj, ck, di, dj, dk):
    """
    Prevent a diagonal move from slicing through a blocked corner/edge: each
    single-axis neighbour involved in the move must itself be free. This keeps
    A* consistent with the straight-line collision check used for shortcutting.
    """
    if di and not grid.is_free((ci + di, cj, ck)):
        return False
    if dj and not grid.is_free((ci, cj + dj, ck)):
        return False
    if dk and not grid.is_free((ci, cj, ck + dk)):
        return False
    return True


def astar(grid, start_world, goal_world, max_expansions=2_000_000):
    start = grid.world_to_grid(grid.clamp_to_bounds(start_world))
    goal = grid.world_to_grid(grid.clamp_to_bounds(goal_world))

    if not grid.is_free(start):
        start = _nearest_free(grid, start)
    if not grid.is_free(goal):
        goal = _nearest_free(grid, goal)
    if start is None or goal is None:
        return None

    def h(a):
        return np.sqrt((a[0] - goal[0]) ** 2 + (a[1] - goal[1]) ** 2 + (a[2] - goal[2]) ** 2)

    open_heap = [(h(start), 0.0, start)]
    came_from = {}
    g_score = {start: 0.0}
    closed = set()
    expansions = 0

    while open_heap:
        _, g_cur, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)
        if cur == goal:
            return _reconstruct(grid, came_from, cur)

        expansions += 1
        if expansions > max_expansions:
            return None

        ci, cj, ck = cur
        for di, dj, dk in _NEIGHBORS:
            nb = (ci + di, cj + dj, ck + dk)
            if nb in closed or not grid.is_free(nb):
                continue
            if not _no_corner_cut(grid, ci, cj, ck, di, dj, dk):
                continue
            step = np.sqrt(di * di + dj * dj + dk * dk)
            tentative = g_cur + step
            if tentative < g_score.get(nb, np.inf):
                g_score[nb] = tentative
                came_from[nb] = cur
                heapq.heappush(open_heap, (tentative + h(nb), tentative, nb))

    return None


def _reconstruct(grid, came_from, cur):
    idxs = [cur]
    while cur in came_from:
        cur = came_from[cur]
        idxs.append(cur)
    idxs.reverse()
    return [grid.grid_to_world(i) for i in idxs]


def _nearest_free(grid, idx, max_r=6):
    """Spiral out from a blocked cell to the closest free voxel."""
    if grid.is_free(idx):
        return idx
    i0, j0, k0 = idx
    for r in range(1, max_r + 1):
        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):
                for dk in range(-r, r + 1):
                    cand = (i0 + di, j0 + dj, k0 + dk)
                    if grid.is_free(cand):
                        return cand
    return None


# ── RRT ─────────────────────────────────────────────────────────────────────
def rrt(grid, start_world, goal_world, step=1.0, goal_bias=0.15,
        max_iters=8000, goal_tol=1.0, seed=1):
    rng = np.random.default_rng(seed)
    start = grid.clamp_to_bounds(np.asarray(start_world, float))
    goal = grid.clamp_to_bounds(np.asarray(goal_world, float))

    nodes = [start]
    parent = {0: None}

    lo = np.array([grid.xmin, grid.ymin, grid.zmin])
    hi = np.array([grid.xmax, grid.ymax, grid.zmax])

    for _ in range(max_iters):
        sample = goal if rng.random() < goal_bias else lo + rng.random(3) * (hi - lo)

        node_arr = np.array(nodes)
        d = np.linalg.norm(node_arr - sample, axis=1)
        n_idx = int(np.argmin(d))
        near = nodes[n_idx]

        direction = sample - near
        dist = np.linalg.norm(direction)
        if dist < 1e-6:
            continue
        new = near + direction / dist * min(step, dist)

        if not grid.is_free(grid.world_to_grid(new)):
            continue
        if not _segment_free(grid, near, new):
            continue

        nodes.append(new)
        parent[len(nodes) - 1] = n_idx

        if np.linalg.norm(new - goal) <= goal_tol and _segment_free(grid, new, goal):
            nodes.append(goal)
            parent[len(nodes) - 1] = len(nodes) - 2
            return _rrt_path(nodes, parent)

    return None


def _rrt_path(nodes, parent):
    idx = len(nodes) - 1
    path = []
    while idx is not None:
        path.append(nodes[idx])
        idx = parent[idx]
    path.reverse()
    return path


def path_length(path):
    if path is None or len(path) < 2:
        return 0.0
    p = np.asarray(path)
    return float(np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1)))
