#!/usr/bin/env python3
import struct

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import Path
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray

from .occupancy_grid import OccupancyGrid3D
from . import planners


class GlobalPlannerNode(Node):

    def __init__(self):
        super().__init__("global_planner_node")

        # ── parameters ────────────────────────────────────────────────────────
        self.declare_parameter("frame_id", "map")
        self.declare_parameter("algorithm", "astar")          # astar | rrt
        self.declare_parameter("resolution", 0.5)
        self.declare_parameter("bounds", [-2.0, 30.0, -15.0, 15.0, 0.0, 12.0])
        self.declare_parameter("robot_radius", 0.6)
        self.declare_parameter("altitude_min", 1.5)
        self.declare_parameter("altitude_max", 10.0)
        self.declare_parameter("start", [0.0, 0.0, 2.0])
        self.declare_parameter("goal", [28.0, 0.0, 3.0])
        # obstacles as a flat list [cx,cy,cz,sx,sy,sz, cx,cy,cz,sx,sy,sz, ...]
        self.declare_parameter("obstacles", [14.0, 0.0, 5.0, 2.0, 18.0, 10.0])
        # no-fly cylinders as flat list [cx,cy,radius,zmin,zmax, ...]
        self.declare_parameter("no_fly_zones", [20.0, 6.0, 3.0, 0.0, 12.0])
        self.declare_parameter("use_live_cloud", False)
        self.declare_parameter("cloud_topic", "/point_cloud/obstacles")
        self.declare_parameter("auto_plan", True)             # plan once on startup

        g = lambda n: self.get_parameter(n).value
        self.frame_id = g("frame_id")
        self.algorithm = g("algorithm")
        self.resolution = g("resolution")
        self.bounds = list(g("bounds"))
        self.robot_radius = g("robot_radius")
        self.alt_min = g("altitude_min")
        self.alt_max = g("altitude_max")
        self.start = np.array(g("start"), float)
        self.goal = np.array(g("goal"), float)
        self.obstacles = list(g("obstacles"))
        self.no_fly = list(g("no_fly_zones"))
        self.use_live_cloud = g("use_live_cloud")

        latched = QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE,
                             durability=DurabilityPolicy.TRANSIENT_LOCAL,
                             history=HistoryPolicy.KEEP_LAST)
        self.path_pub = self.create_publisher(Path, "/planner/path", latched)
        self.marker_pub = self.create_publisher(MarkerArray, "/planner/markers", latched)

        self.create_subscription(PoseStamped, "/planner/goal", self._goal_cb, 10)

        # optional start from MAVROS local position
        self.have_pose = False
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb,
            QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT,
                       history=HistoryPolicy.KEEP_LAST))

        self.live_points = None
        if self.use_live_cloud:
            self.create_subscription(
                PointCloud2, g("cloud_topic"), self._cloud_cb,
                QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT,
                           history=HistoryPolicy.KEEP_LAST))
            try:
                from tf2_ros import Buffer, TransformListener
                self.tf_buffer = Buffer()
                self.tf_listener = TransformListener(self.tf_buffer, self)
            except Exception as e:
                self.get_logger().warn(f"TF unavailable, live cloud disabled: {e}")
                self.use_live_cloud = False

        self.get_logger().info(
            f"GlobalPlannerNode ready (algorithm={self.algorithm}, frame={self.frame_id}).")

        if g("auto_plan"):
            self.create_timer(2.0, self._plan_once)

    # ── callbacks ─────────────────────────────────────────────────────────────
    def _pose_cb(self, msg: PoseStamped):
        self.start = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])
        self.have_pose = True

    def _goal_cb(self, msg: PoseStamped):
        self.goal = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])
        self.get_logger().info(f"New goal: {self.goal.round(2).tolist()}")
        self.plan()

    def _cloud_cb(self, msg: PointCloud2):
        pts = self._read_xyz(msg)
        if pts is None or len(pts) == 0:
            return
        # transform into the planning frame if needed
        if msg.header.frame_id and msg.header.frame_id != self.frame_id and self.use_live_cloud:
            try:
                from tf2_ros import TransformException
                tf = self.tf_buffer.lookup_transform(
                    self.frame_id, msg.header.frame_id, rclpy.time.Time())
                pts = self._apply_tf(pts, tf)
            except Exception:
                return  # no transform yet; skip this cloud
        self.live_points = pts

    # ── planning ──────────────────────────────────────────────────────────────
    def _plan_once(self):
        # timer fires once then cancels
        for t in list(self.timers):
            t.cancel()
        self.plan()

    def build_grid(self):
        grid = OccupancyGrid3D(self.bounds, self.resolution)
        for i in range(0, len(self.obstacles) - 5, 6):
            c = self.obstacles[i:i + 3]
            s = self.obstacles[i + 3:i + 6]
            grid.add_box(c, s)
        for i in range(0, len(self.no_fly) - 4, 5):
            cx, cy, r, zmin, zmax = self.no_fly[i:i + 5]
            grid.add_cylinder_zone(cx, cy, r, zmin, zmax)
        if self.use_live_cloud and self.live_points is not None:
            grid.add_points(self.live_points)
        grid.inflate(self.robot_radius)                 # inflate obstacles ...
        grid.add_altitude_limits(self.alt_min, self.alt_max)  # ... then corridor
        return grid

    def plan(self):
        grid = self.build_grid()
        self.get_logger().info(
            f"Planning {self.algorithm}: start={self.start.round(2).tolist()} "
            f"goal={self.goal.round(2).tolist()}")

        if self.algorithm == "rrt":
            raw = planners.rrt(grid, self.start, self.goal)
        else:
            raw = planners.astar(grid, self.start, self.goal)

        if raw is None:
            self.get_logger().error("No path found! Check bounds / obstacles / altitude limits.")
            self._publish_markers(grid, path=None)
            return

        path = planners.shortcut(grid, raw)
        length = planners.path_length(path)
        self.get_logger().info(
            f"Path found: {len(raw)} raw -> {len(path)} waypoints, length {length:.1f} m")

        self._publish_path(path)
        self._publish_markers(grid, path)

    # ── publishing ────────────────────────────────────────────────────────────
    def _publish_path(self, path):
        msg = Path()
        msg.header.frame_id = self.frame_id
        msg.header.stamp = self.get_clock().now().to_msg()
        for wp in path:
            ps = PoseStamped()
            ps.header = msg.header
            ps.pose.position.x = float(wp[0])
            ps.pose.position.y = float(wp[1])
            ps.pose.position.z = float(wp[2])
            ps.pose.orientation.w = 1.0
            msg.poses.append(ps)
        self.path_pub.publish(msg)

    def _publish_markers(self, grid, path):
        arr = MarkerArray()
        stamp = self.get_clock().now().to_msg()

        # occupied voxels as a cube list (sampled to keep marker light)
        occ = grid.occupied_centers()
        if len(occ) > 20000:
            occ = occ[:: len(occ) // 20000 + 1]
        m = Marker()
        m.header.frame_id = self.frame_id
        m.header.stamp = stamp
        m.ns = "occupancy"
        m.id = 0
        m.type = Marker.CUBE_LIST
        m.action = Marker.ADD
        m.scale.x = m.scale.y = m.scale.z = grid.res * 0.9
        m.color = ColorRGBA(r=0.5, g=0.5, b=0.55, a=0.25)
        m.points = [Point(x=float(p[0]), y=float(p[1]), z=float(p[2])) for p in occ]
        arr.markers.append(m)

        # start & goal spheres
        for i, (pos, col) in enumerate([(self.start, (0.1, 0.8, 1.0)), (self.goal, (1.0, 0.85, 0.1))]):
            s = Marker()
            s.header.frame_id = self.frame_id
            s.header.stamp = stamp
            s.ns = "endpoints"
            s.id = i + 1
            s.type = Marker.SPHERE
            s.action = Marker.ADD
            s.pose.position.x, s.pose.position.y, s.pose.position.z = map(float, pos)
            s.pose.orientation.w = 1.0
            s.scale.x = s.scale.y = s.scale.z = 0.8
            s.color = ColorRGBA(r=col[0], g=col[1], b=col[2], a=1.0)
            arr.markers.append(s)

        # path as a line strip
        if path is not None:
            line = Marker()
            line.header.frame_id = self.frame_id
            line.header.stamp = stamp
            line.ns = "path"
            line.id = 10
            line.type = Marker.LINE_STRIP
            line.action = Marker.ADD
            line.scale.x = 0.15
            line.color = ColorRGBA(r=0.1, g=1.0, b=0.3, a=1.0)
            line.points = [Point(x=float(p[0]), y=float(p[1]), z=float(p[2])) for p in path]
            arr.markers.append(line)

        self.marker_pub.publish(arr)

    # ── PointCloud2 helpers ───────────────────────────────────────────────────
    @staticmethod
    def _read_xyz(msg: PointCloud2):
        # generic XYZ reader (assumes float32 x,y,z at offsets 0,4,8)
        if msg.point_step < 12:
            return None
        n = msg.width * msg.height
        buf = np.frombuffer(msg.data, dtype=np.uint8).reshape(n, msg.point_step)
        xyz = np.frombuffer(buf[:, 0:12].tobytes(), dtype=np.float32).reshape(n, 3)
        good = np.isfinite(xyz).all(axis=1)
        return xyz[good]

    @staticmethod
    def _apply_tf(pts, tf):
        t = tf.transform.translation
        q = tf.transform.rotation
        # quaternion -> rotation matrix
        x, y, z, w = q.x, q.y, q.z, q.w
        R = np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ])
        return (R @ pts.T).T + np.array([t.x, t.y, t.z])


def main(args=None):
    rclpy.init(args=args)
    node = GlobalPlannerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        # ros2 launch may have already shut the context down on SIGINT
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
