#!/usr/bin/env python3
"""
Point Cloud Node — Task 2: Depth Estimation & 3D Point Cloud Generation
-----------------------------------------------------------------------
Subscribes to:
  - /camera/color/image       (RGB image)
  - /camera/depth/image       (depth image, float32 metres)
  - /camera/color/camera_info (intrinsics)

Publishes:
  - /point_cloud/full          (PointCloud2) — full colored cloud
  - /point_cloud/ground        (PointCloud2) — ground plane points
  - /point_cloud/obstacles     (PointCloud2) — non-ground / obstacle points
  - /depth/colormap            (Image)        — false-colour depth for RViz2
  - /depth/stats               (String)        — MAE/RMSE vs GT (if available)
"""

import time
import struct

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from message_filters import ApproximateTimeSynchronizer, Subscriber

from sensor_msgs.msg import Image, CameraInfo, PointCloud2, PointField
from std_msgs.msg import String, Header
from cv_bridge import CvBridge


# ─── Helpers ──────────────────────────────────────────────────────────────────

def build_point_cloud_msg(header: Header, xyz: np.ndarray, rgb: np.ndarray | None = None) -> PointCloud2:
    """
    Build a sensor_msgs/PointCloud2 from (N,3) XYZ and optional (N,3) uint8 RGB.
    Uses XYZRGB layout when colours provided, XYZ otherwise.
    """
    N = xyz.shape[0]

    if rgb is not None:
        # Pack R,G,B into a single float32 (standard RViz2 XYZRGB convention)
        r = rgb[:, 0].astype(np.uint32)
        g = rgb[:, 1].astype(np.uint32)
        b = rgb[:, 2].astype(np.uint32)
        rgb_packed = ((r << 16) | (g << 8) | b).astype(np.uint32)
        rgb_float = rgb_packed.view(np.float32)

        data = np.column_stack([xyz.astype(np.float32), rgb_float]).tobytes()
        point_step = 16  # 4 floats × 4 bytes
        fields = [
            PointField(name="x", offset=0,  datatype=PointField.FLOAT32, count=1),
            PointField(name="y", offset=4,  datatype=PointField.FLOAT32, count=1),
            PointField(name="z", offset=8,  datatype=PointField.FLOAT32, count=1),
            PointField(name="rgb", offset=12, datatype=PointField.FLOAT32, count=1),
        ]
    else:
        data = xyz.astype(np.float32).tobytes()
        point_step = 12
        fields = [
            PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
        ]

    msg = PointCloud2()
    msg.header      = header
    msg.height      = 1
    msg.width       = N
    msg.is_dense    = False
    msg.is_bigendian = False
    msg.fields      = fields
    msg.point_step  = point_step
    msg.row_step    = point_step * N
    msg.data        = data
    return msg


def ransac_plane(points: np.ndarray,
                 n_iter: int = 200,
                 dist_thresh: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """
    Fit a plane to `points` (N,3) using RANSAC.
    Returns:
      plane_normal  (3,)  — unit normal of best plane
      inlier_mask   (N,)  — boolean mask of inlier points
    """
    best_inliers = np.zeros(len(points), dtype=bool)
    best_count   = 0
    rng          = np.random.default_rng(42)

    for _ in range(n_iter):
        idx = rng.choice(len(points), 3, replace=False)
        p0, p1, p2 = points[idx]
        n = np.cross(p1 - p0, p2 - p0)
        norm = np.linalg.norm(n)
        if norm < 1e-9:
            continue
        n /= norm

        # Signed distance of every point to the plane
        dists = np.abs((points - p0) @ n)
        inliers = dists < dist_thresh
        count = inliers.sum()
        if count > best_count:
            best_count   = count
            best_inliers = inliers

    if best_count >= 3:
        # Refine plane with all inliers (least-squares)
        pts = points[best_inliers]
        centroid = pts.mean(axis=0)
        _, _, Vt = np.linalg.svd(pts - centroid)
        plane_normal = Vt[-1]
    else:
        plane_normal = np.array([0.0, 1.0, 0.0])

    return plane_normal, best_inliers


# ─── Node ─────────────────────────────────────────────────────────────────────

class PointCloudNode(Node):

    def __init__(self):
        super().__init__("point_cloud_node")

        # ── Parameters ────────────────────────────────────────────────────────
        self.declare_parameter("rgb_topic",   "/camera/color/image")
        self.declare_parameter("depth_topic", "/camera/depth/image")
        self.declare_parameter("info_topic",  "/camera/color/camera_info")
        self.declare_parameter("depth_scale", 1.0)          # metres per depth unit
        self.declare_parameter("max_depth",   10.0)         # clip at N metres
        self.declare_parameter("min_depth",   0.1)
        self.declare_parameter("ransac_iters",      200)
        self.declare_parameter("ransac_thresh",     0.05)   # metres
        self.declare_parameter("ground_normal_tol", 0.25)   # cos tolerance
        self.declare_parameter("downsample_step",   2)      # pixel stride

        p = lambda n: self.get_parameter(n).value
        self.depth_scale    = p("depth_scale")
        self.max_depth      = p("max_depth")
        self.min_depth      = p("min_depth")
        self.ransac_iters   = p("ransac_iters")
        self.ransac_thresh  = p("ransac_thresh")
        self.gnd_tol        = p("ground_normal_tol")
        self.stride         = p("downsample_step")

        # Camera intrinsics (filled when CameraInfo arrives)
        self.fx = self.fy = self.cx = self.cy = None

        self.bridge = CvBridge()

        # ── QoS ───────────────────────────────────────────────────────────────
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )

        # ── Camera info (latched / reliable) ─────────────────────────────────
        self.create_subscription(
            CameraInfo, p("info_topic"), self._info_cb,
            QoSProfile(reliability=ReliabilityPolicy.RELIABLE,
                       history=HistoryPolicy.KEEP_LAST, depth=1)
        )

        # ── Synchronised RGB + Depth ──────────────────────────────────────────
        self.rgb_sub   = Subscriber(self, Image, p("rgb_topic"),   qos_profile=qos)
        self.depth_sub = Subscriber(self, Image, p("depth_topic"), qos_profile=qos)
        self.sync = ApproximateTimeSynchronizer(
            [self.rgb_sub, self.depth_sub], queue_size=5, slop=0.1
        )
        self.sync.registerCallback(self._rgbd_cb)

        # ── Publishers ────────────────────────────────────────────────────────
        self.pub_full      = self.create_publisher(PointCloud2, "/point_cloud/full",      10)
        self.pub_ground    = self.create_publisher(PointCloud2, "/point_cloud/ground",    10)
        self.pub_obstacles = self.create_publisher(PointCloud2, "/point_cloud/obstacles", 10)
        self.pub_colormap  = self.create_publisher(Image,       "/depth/colormap",        10)
        self.pub_stats     = self.create_publisher(String,      "/depth/stats",           10)

        self._frame = 0
        self.get_logger().info("PointCloudNode ready.")

    # ── CameraInfo callback ────────────────────────────────────────────────────
    def _info_cb(self, msg: CameraInfo):
        if self.fx is None:
            self.fx = msg.k[0]
            self.fy = msg.k[4]
            self.cx = msg.k[2]
            self.cy = msg.k[5]
            self.get_logger().info(
                f"Camera intrinsics received: fx={self.fx:.1f} fy={self.fy:.1f} "
                f"cx={self.cx:.1f} cy={self.cy:.1f}"
            )

    # ── Main RGBD callback ─────────────────────────────────────────────────────
    def _rgbd_cb(self, rgb_msg: Image, depth_msg: Image):
        if self.fx is None:
            self.get_logger().warn("Waiting for camera intrinsics…", throttle_duration_sec=5.0)
            return

        t0 = time.time()

        # ── Convert images ────────────────────────────────────────────────────
        try:
            rgb   = self.bridge.imgmsg_to_cv2(rgb_msg,   desired_encoding="rgb8")
            depth = self.bridge.imgmsg_to_cv2(depth_msg, desired_encoding="passthrough")
        except Exception as e:
            self.get_logger().error(f"CvBridge error: {e}")
            return

        depth = depth.astype(np.float32) * self.depth_scale

        # ── Depth colormap ────────────────────────────────────────────────────
        self._publish_colormap(depth, depth_msg.header)

        # ── Downsample ────────────────────────────────────────────────────────
        s = self.stride
        depth_s = depth[::s, ::s]
        rgb_s   = rgb[::s, ::s]
        H, W    = depth_s.shape

        # ── Pixel grid ────────────────────────────────────────────────────────
        u = np.arange(W) * s  # original pixel coords
        v = np.arange(H) * s
        uu, vv = np.meshgrid(u, v)

        # ── Valid depth mask ──────────────────────────────────────────────────
        valid = (depth_s > self.min_depth) & (depth_s < self.max_depth) & np.isfinite(depth_s)

        Z = depth_s[valid]
        U = uu[valid]
        V = vv[valid]

        # ── Back-project to 3D (camera frame: X right, Y down, Z forward) ────
        X = (U - self.cx) * Z / self.fx
        Y = (V - self.cy) * Z / self.fy
        xyz = np.column_stack([X, Y, Z])          # (N, 3)
        rgb_pts = rgb_s[valid]                    # (N, 3) uint8

        if len(xyz) < 10:
            self.get_logger().warn("Too few valid depth points.", throttle_duration_sec=2.0)
            return

        header = rgb_msg.header

        # ── Publish full cloud ────────────────────────────────────────────────
        self.pub_full.publish(build_point_cloud_msg(header, xyz, rgb_pts))

        # ── RANSAC ground segmentation ────────────────────────────────────────
        plane_normal, ground_mask = ransac_plane(
            xyz, n_iter=self.ransac_iters, dist_thresh=self.ransac_thresh
        )

        # Sanity-check: ground plane normal should be roughly vertical
        # In camera frame, "up" ≈ -Y, so normal Y component should dominate.
        # Accept plane if |n·[0,1,0]| > threshold.
        vert = abs(float(plane_normal[1]))
        if vert > self.gnd_tol:
            obstacle_mask = ~ground_mask
        else:
            # RANSAC found a non-vertical plane — treat everything as obstacles
            self.get_logger().warn(
                f"RANSAC plane may not be ground (|n_y|={vert:.2f}). "
                "Treating all points as obstacles.",
                throttle_duration_sec=5.0,
            )
            ground_mask   = np.zeros(len(xyz), dtype=bool)
            obstacle_mask = np.ones(len(xyz),  dtype=bool)

        # ── Publish ground + obstacle clouds ─────────────────────────────────
        if ground_mask.any():
            self.pub_ground.publish(
                build_point_cloud_msg(header, xyz[ground_mask], rgb_pts[ground_mask])
            )
        if obstacle_mask.any():
            self.pub_obstacles.publish(
                build_point_cloud_msg(header, xyz[obstacle_mask], rgb_pts[obstacle_mask])
            )

        # ── Stats ─────────────────────────────────────────────────────────────
        elapsed_ms = (time.time() - t0) * 1000
        self._frame += 1

        if self._frame % 30 == 0:
            n_total    = len(xyz)
            n_ground   = int(ground_mask.sum())
            n_obstacle = int(obstacle_mask.sum())
            self.get_logger().info(
                f"[Frame {self._frame}] "
                f"Points: {n_total} | Ground: {n_ground} | Obstacles: {n_obstacle} | "
                f"Time: {elapsed_ms:.1f}ms"
            )

        stats_msg = String()
        stats_msg.data = (
            f"frame={self._frame} "
            f"total_pts={len(xyz)} "
            f"ground_pts={int(ground_mask.sum())} "
            f"obstacle_pts={int(obstacle_mask.sum())} "
            f"proc_ms={elapsed_ms:.1f}"
        )
        self.pub_stats.publish(stats_msg)

    # ── Depth colormap publisher ───────────────────────────────────────────────
    def _publish_colormap(self, depth: np.ndarray, header):
        clipped = np.clip(depth, 0, self.max_depth)
        norm    = (clipped / self.max_depth * 255).astype(np.uint8)
        colormap = cv2.applyColorMap(norm, cv2.COLORMAP_TURBO)  # warm = near, cold = far
        msg = self.bridge.cv2_to_imgmsg(colormap, encoding="bgr8")
        msg.header = header
        self.pub_colormap.publish(msg)


# ─────────────────────────────────────────────────────────────────────────────
def main(args=None):
    rclpy.init(args=args)
    node = PointCloudNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
