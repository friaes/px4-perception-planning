import time

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import CameraInfo, Image, PointCloud2, PointField
from std_msgs.msg import Header, String


def build_point_cloud_msg(header, xyz, rgb=None):
    N = xyz.shape[0]
    if rgb is not None:
        r = rgb[:, 0].astype(np.uint32)
        g = rgb[:, 1].astype(np.uint32)
        b = rgb[:, 2].astype(np.uint32)
        rgb_float = ((r << 16) | (g << 8) | b).astype(np.uint32).view(np.float32)
        data = np.column_stack([xyz.astype(np.float32), rgb_float]).astype(np.float32).tobytes()
        point_step = 16
        fields = [
            PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
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
    msg.header = header
    msg.height = 1
    msg.width = N
    msg.is_dense = False
    msg.is_bigendian = False
    msg.fields = fields
    msg.point_step = point_step
    msg.row_step = point_step * N
    msg.data = data
    return msg


def ransac_plane_fit(points, n_iter=100, dist_thresh=0.05, rng=None):
    """
    Fit a plane to `points` with RANSAC.
    Returns (unit_normal, point_on_plane). Classification of the full cloud is
    done by the caller using the returned plane.
    """
    rng = rng or np.random.default_rng(42)
    best_inliers = None
    best_count = 0

    for _ in range(n_iter):
        idx = rng.choice(len(points), 3, replace=False)
        p0, p1, p2 = points[idx]
        n = np.cross(p1 - p0, p2 - p0)
        norm = np.linalg.norm(n)
        if norm < 1e-9:
            continue
        n /= norm
        dists = np.abs((points - p0) @ n)
        inliers = dists < dist_thresh
        count = int(inliers.sum())
        if count > best_count:
            best_count = count
            best_inliers = inliers

    if best_inliers is not None and best_count >= 3:
        pts = points[best_inliers]
        centroid = pts.mean(axis=0)
        _, _, Vt = np.linalg.svd(pts - centroid)
        return Vt[-1], centroid
    return np.array([0.0, 1.0, 0.0]), points.mean(axis=0)


class PointCloudNode(Node):

    def __init__(self):
        super().__init__("point_cloud_node")

        self.declare_parameter("rgb_topic", "/camera/color/image")
        self.declare_parameter("depth_topic", "/camera/depth/image")
        self.declare_parameter("info_topic", "/camera/color/camera_info")
        self.declare_parameter("output_frame", "camera_link")
        self.declare_parameter("depth_scale", 1.0)
        self.declare_parameter("max_depth", 10.0)
        self.declare_parameter("min_depth", 0.1)
        self.declare_parameter("ransac_iters", 100)
        self.declare_parameter("ransac_thresh", 0.05)
        self.declare_parameter("ransac_sample", 4000)      # points used to FIT the plane
        self.declare_parameter("ground_normal_tol", 0.25)
        self.declare_parameter("downsample_step", 4)       # 1920x1080 -> stride 4 ~= 130k pts

        p = lambda n: self.get_parameter(n).value
        self.output_frame = p("output_frame")
        self.depth_scale = p("depth_scale")
        self.max_depth = p("max_depth")
        self.min_depth = p("min_depth")
        self.ransac_iters = int(p("ransac_iters"))
        self.ransac_thresh = p("ransac_thresh")
        self.ransac_sample = int(p("ransac_sample"))
        self.gnd_tol = p("ground_normal_tol")
        self.stride = int(p("downsample_step"))

        self.fx = self.fy = self.cx = self.cy = None
        self.bridge = CvBridge()
        self.latest_rgb = None
        self._rng = np.random.default_rng(0)

        # Sensor QoS for inputs
        in_qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                            history=HistoryPolicy.KEEP_LAST, depth=1)
        # Output QoS: best-effort keep-last-1 so big clouds are DROPPED, not buffered
        out_qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                             history=HistoryPolicy.KEEP_LAST, depth=1)

        self.create_subscription(
            CameraInfo, p("info_topic"), self._info_cb,
            QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=1))
        self.create_subscription(Image, p("rgb_topic"), self._rgb_cb, in_qos)
        self.create_subscription(Image, p("depth_topic"), self._depth_cb, in_qos)

        self.pub_full = self.create_publisher(PointCloud2, "/point_cloud/full", out_qos)
        self.pub_ground = self.create_publisher(PointCloud2, "/point_cloud/ground", out_qos)
        self.pub_obstacles = self.create_publisher(PointCloud2, "/point_cloud/obstacles", out_qos)
        self.pub_colormap = self.create_publisher(Image, "/depth/colormap", out_qos)
        self.pub_stats = self.create_publisher(String, "/depth/stats", 10)

        self._frame = 0
        self.get_logger().info("PointCloudNode ready.")

    def _info_cb(self, msg: CameraInfo):
        if self.fx is None:
            self.fx, self.fy, self.cx, self.cy = msg.k[0], msg.k[4], msg.k[2], msg.k[5]
            self.get_logger().info(
                f"Camera intrinsics received: fx={self.fx:.1f} fy={self.fy:.1f} cx={self.cx:.1f} cy={self.cy:.1f}")

    def _rgb_cb(self, msg: Image):
        try:
            self.latest_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
        except Exception as e:
            self.get_logger().error(f"RGB CvBridge error: {e}")

    def _depth_cb(self, depth_msg: Image):
        if self.fx is None:
            self.get_logger().warn("Waiting for camera intrinsics...", throttle_duration_sec=5.0)
            return

        t0 = time.time()
        try:
            depth = self.bridge.imgmsg_to_cv2(depth_msg, desired_encoding="passthrough").astype(np.float32)
        except Exception as e:
            self.get_logger().error(f"Depth CvBridge error: {e}")
            return
        depth *= self.depth_scale

        if self.latest_rgb is not None:
            rgb = self.latest_rgb
            if rgb.shape[:2] != depth.shape[:2]:
                rgb = cv2.resize(rgb, (depth.shape[1], depth.shape[0]), interpolation=cv2.INTER_NEAREST)
        else:
            rgb = np.full((depth.shape[0], depth.shape[1], 3), 180, dtype=np.uint8)

        self._publish_colormap(depth, depth_msg.header)

        s = self.stride
        depth_s = depth[::s, ::s]
        rgb_s = rgb[::s, ::s]
        H, W = depth_s.shape

        u = np.arange(W) * s
        v = np.arange(H) * s
        uu, vv = np.meshgrid(u, v)

        valid = (depth_s > self.min_depth) & (depth_s < self.max_depth) & np.isfinite(depth_s)
        Z = depth_s[valid]
        U = uu[valid]
        V = vv[valid]

        X = (U - self.cx) * Z / self.fx
        Y = (V - self.cy) * Z / self.fy
        xyz = np.column_stack([X, Y, Z])
        rgb_pts = rgb_s[valid]

        if len(xyz) < 10:
            self.get_logger().warn("Too few valid depth points.", throttle_duration_sec=2.0)
            return

        header = Header()
        header.stamp = depth_msg.header.stamp
        header.frame_id = self.output_frame

        self.pub_full.publish(build_point_cloud_msg(header, xyz, rgb_pts))

        # --- RANSAC: fit on a subset, classify ALL points against the plane ---
        if len(xyz) > self.ransac_sample:
            sub = self._rng.choice(len(xyz), self.ransac_sample, replace=False)
            fit_pts = xyz[sub]
        else:
            fit_pts = xyz

        normal, plane_pt = ransac_plane_fit(
            fit_pts, n_iter=self.ransac_iters, dist_thresh=self.ransac_thresh, rng=self._rng)

        dist_all = np.abs((xyz - plane_pt) @ normal)
        ground_mask = dist_all < self.ransac_thresh

        if abs(float(normal[1])) > self.gnd_tol:
            obstacle_mask = ~ground_mask
        else:
            self.get_logger().warn(
                f"RANSAC plane may not be ground (|n_y|={abs(float(normal[1])):.2f}). All points -> obstacles.",
                throttle_duration_sec=5.0)
            ground_mask = np.zeros(len(xyz), dtype=bool)
            obstacle_mask = np.ones(len(xyz), dtype=bool)

        if ground_mask.any():
            self.pub_ground.publish(build_point_cloud_msg(header, xyz[ground_mask], rgb_pts[ground_mask]))
        if obstacle_mask.any():
            self.pub_obstacles.publish(build_point_cloud_msg(header, xyz[obstacle_mask], rgb_pts[obstacle_mask]))

        elapsed_ms = (time.time() - t0) * 1000
        self._frame += 1
        if self._frame % 15 == 0:
            self.get_logger().info(
                f"[Frame {self._frame}] Points: {len(xyz)} | Ground: {int(ground_mask.sum())} | "
                f"Obstacles: {int(obstacle_mask.sum())} | Time: {elapsed_ms:.1f}ms")

        stats = String()
        stats.data = (f"frame={self._frame} total_pts={len(xyz)} ground_pts={int(ground_mask.sum())} "
                      f"obstacle_pts={int(obstacle_mask.sum())} proc_ms={elapsed_ms:.1f}")
        self.pub_stats.publish(stats)

    def _publish_colormap(self, depth, header):
        clipped = np.clip(np.nan_to_num(depth, nan=0.0), 0, self.max_depth)
        norm = (clipped / self.max_depth * 255).astype(np.uint8)
        colormap = cv2.applyColorMap(norm, cv2.COLORMAP_TURBO)
        msg = self.bridge.cv2_to_imgmsg(colormap, encoding="bgr8")
        msg.header.stamp = header.stamp
        msg.header.frame_id = self.output_frame
        self.pub_colormap.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PointCloudNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()