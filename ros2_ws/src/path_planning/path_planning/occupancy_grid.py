#!/usr/bin/env python3
from __future__ import annotations

import numpy as np


class OccupancyGrid3D:
    def __init__(self, bounds, resolution=0.5):
        """
        bounds: (xmin, xmax, ymin, ymax, zmin, zmax) in metres
        resolution: voxel edge length in metres
        """
        self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = map(float, bounds)
        self.res = float(resolution)

        self.nx = max(1, int(np.ceil((self.xmax - self.xmin) / self.res)))
        self.ny = max(1, int(np.ceil((self.ymax - self.ymin) / self.res)))
        self.nz = max(1, int(np.ceil((self.zmax - self.zmin) / self.res)))

        self.grid = np.zeros((self.nx, self.ny, self.nz), dtype=bool)
        self.origin = np.array([self.xmin, self.ymin, self.zmin], dtype=float)

    # ── coordinate conversion ────────────────────────────────────────────────
    def world_to_grid(self, p):
        idx = np.floor((np.asarray(p, float) - self.origin) / self.res).astype(int)
        return tuple(idx)

    def grid_to_world(self, idx):
        # centre of the voxel
        return self.origin + (np.asarray(idx, float) + 0.5) * self.res

    def in_bounds(self, idx):
        i, j, k = idx
        return 0 <= i < self.nx and 0 <= j < self.ny and 0 <= k < self.nz

    def is_free(self, idx):
        if not self.in_bounds(idx):
            return False
        return not self.grid[idx[0], idx[1], idx[2]]

    def clamp_to_bounds(self, p):
        p = np.asarray(p, float).copy()
        p[0] = np.clip(p[0], self.xmin, self.xmax - 1e-3)
        p[1] = np.clip(p[1], self.ymin, self.ymax - 1e-3)
        p[2] = np.clip(p[2], self.zmin, self.zmax - 1e-3)
        return p

    # ── population ───────────────────────────────────────────────────────────
    def _voxel_centers(self):
        xs = self.xmin + (np.arange(self.nx) + 0.5) * self.res
        ys = self.ymin + (np.arange(self.ny) + 0.5) * self.res
        zs = self.zmin + (np.arange(self.nz) + 0.5) * self.res
        return xs, ys, zs

    def add_box(self, center, size):
        """Axis-aligned box obstacle. center=(x,y,z), size=(sx,sy,sz) full extents."""
        cx, cy, cz = center
        sx, sy, sz = size
        xs, ys, zs = self._voxel_centers()
        mx = np.abs(xs - cx) <= sx / 2
        my = np.abs(ys - cy) <= sy / 2
        mz = np.abs(zs - cz) <= sz / 2
        self.grid[np.ix_(mx, my, mz)] = True

    def add_cylinder_zone(self, cx, cy, radius, z_min=None, z_max=None):
        """Vertical-cylinder no-fly zone (great for keep-out around a point)."""
        z_min = self.zmin if z_min is None else z_min
        z_max = self.zmax if z_max is None else z_max
        xs, ys, zs = self._voxel_centers()
        XX, YY = np.meshgrid(xs, ys, indexing="ij")
        disk = (XX - cx) ** 2 + (YY - cy) ** 2 <= radius ** 2   # [nx, ny]
        mz = (zs >= z_min) & (zs <= z_max)
        self.grid[disk[:, :, None] & mz[None, None, :]] = True

    def add_altitude_limits(self, z_min_flight, z_max_flight):
        """Block everything below z_min_flight and above z_max_flight."""
        _, _, zs = self._voxel_centers()
        below = zs < z_min_flight
        above = zs > z_max_flight
        self.grid[:, :, below | above] = True

    def add_points(self, points_world):
        """Mark voxels containing any of the given (N,3) world points as blocked."""
        pts = np.asarray(points_world, float)
        if pts.size == 0:
            return
        idx = np.floor((pts - self.origin) / self.res).astype(int)
        keep = (
            (idx[:, 0] >= 0) & (idx[:, 0] < self.nx)
            & (idx[:, 1] >= 0) & (idx[:, 1] < self.ny)
            & (idx[:, 2] >= 0) & (idx[:, 2] < self.nz)
        )
        idx = idx[keep]
        if len(idx):
            self.grid[idx[:, 0], idx[:, 1], idx[:, 2]] = True

    def inflate(self, radius_m):
        """
        Dilate obstacles by `radius_m` (robot radius) so the planner keeps a
        safety margin. Implemented as an OR over integer voxel offsets within a
        sphere - cheap for small radii, no scipy dependency.
        """
        r = int(np.ceil(radius_m / self.res))
        if r <= 0:
            return
        base = self.grid.copy()
        out = base.copy()
        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):
                for dk in range(-r, r + 1):
                    if di * di + dj * dj + dk * dk > r * r:
                        continue
                    if di == 0 and dj == 0 and dk == 0:
                        continue
                    shifted = np.zeros_like(base)
                    src = base[
                        max(0, -di):self.nx - max(0, di),
                        max(0, -dj):self.ny - max(0, dj),
                        max(0, -dk):self.nz - max(0, dk),
                    ]
                    shifted[
                        max(0, di):self.nx - max(0, -di),
                        max(0, dj):self.ny - max(0, -dj),
                        max(0, dk):self.nz - max(0, -dk),
                    ] = src
                    out |= shifted
        self.grid = out

    def occupied_centers(self):
        """(M,3) world centres of all occupied voxels (for RViz markers)."""
        ii, jj, kk = np.where(self.grid)
        if len(ii) == 0:
            return np.empty((0, 3))
        return self.origin + (np.stack([ii, jj, kk], axis=1) + 0.5) * self.res
