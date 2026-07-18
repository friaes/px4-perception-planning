#!/usr/bin/env python3
import math

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from geometry_msgs.msg import PoseStamped, TwistStamped, Point
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String, ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray

try:
    from mavros_msgs.msg import State
    from mavros_msgs.srv import CommandBool, SetMode
    MAVROS_OK = True
except Exception:                      # pragma: no cover
    MAVROS_OK = False


class LocalPlannerNode(Node):

    def __init__(self):
        super().__init__("local_planner_node")

        self.declare_parameter("goal", [20.0, 0.0, 3.0])
        self.declare_parameter("v_max", 1.5)               # max speed [m/s]
        self.declare_parameter("k_att", 0.6)               # attractive gain
        self.declare_parameter("k_rep", 0.8)               # repulsive gain
        self.declare_parameter("influence_radius", 4.0)    # d0: repulsion range [m]
        self.declare_parameter("goal_tol", 0.8)            # success radius [m]
        self.declare_parameter("max_points", 1500)         # cap points used for APF
        self.declare_parameter("auto_arm", True)
        self.declare_parameter("cloud_topic", "/point_cloud/obstacles")

        g = lambda n: self.get_parameter(n).value
        self.goal = np.array(g("goal"), float)
        self.v_max = g("v_max")
        self.k_att = g("k_att")
        self.k_rep = g("k_rep")
        self.d0 = g("influence_radius")
        self.goal_tol = g("goal_tol")
        self.max_points = int(g("max_points"))
        self.auto_arm = g("auto_arm")

        self.pose = None
        self.yaw = 0.0
        self.obstacles_flu = None
        self.state = State() if MAVROS_OK else None
        self._last_req = self.get_clock().now()

        # metrics
        self._start_pos = None
        self._traveled = 0.0
        self._prev_pos = None
        self._min_obs_dist = np.inf
        self._reached = False

        sensor = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST)
        self.create_subscription(PointCloud2, g("cloud_topic"), self._cloud_cb, sensor)
        self.create_subscription(PoseStamped, "/mavros/local_position/pose", self._pose_cb, sensor)
        if MAVROS_OK:
            self.create_subscription(State, "/mavros/state", self._state_cb, 10)
            self.vel_pub = self.create_publisher(TwistStamped, "/mavros/setpoint_velocity/cmd_vel", 10)
            self.arm_cli = self.create_client(CommandBool, "/mavros/cmd/arming")
            self.mode_cli = self.create_client(SetMode, "/mavros/set_mode")
        else:
            self.get_logger().error("mavros_msgs missing - velocity setpoints will not be sent.")
            self.vel_pub = None

        self.stats_pub = self.create_publisher(String, "/local_planner/stats", 10)
        self.marker_pub = self.create_publisher(MarkerArray, "/local_planner/markers", 10)

        self.create_timer(0.05, self._tick)     # 20 Hz control loop
        self.get_logger().info(f"LocalPlannerNode (APF) ready. goal={self.goal.round(2).tolist()}")

    # ── callbacks ─────────────────────────────────────────────────────────────
    def _pose_cb(self, msg):
        self.pose = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])
        q = msg.pose.orientation
        self.yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
        if self._start_pos is None:
            self._start_pos = self.pose.copy()
            self._prev_pos = self.pose.copy()
        else:
            self._traveled += np.linalg.norm(self.pose - self._prev_pos)
            self._prev_pos = self.pose.copy()

    def _state_cb(self, msg):
        self.state = msg

    def _cloud_cb(self, msg):
        pts = self._read_xyz(msg)
        if pts is None or len(pts) == 0:
            self.obstacles_flu = None
            return
        if len(pts) > self.max_points:
            idx = np.random.default_rng(0).choice(len(pts), self.max_points, replace=False)
            pts = pts[idx]
        # camera optical (X right, Y down, Z fwd) -> body FLU (X fwd, Y left, Z up)
        flu = np.column_stack([pts[:, 2], -pts[:, 0], -pts[:, 1]])
        self.obstacles_flu = flu
        d = np.linalg.norm(flu, axis=1)
        if len(d):
            self._min_obs_dist = min(self._min_obs_dist, float(d.min()))

    # ── control loop ──────────────────────────────────────────────────────────
    def _tick(self):
        if self.pose is None:
            return

        to_goal = self.goal - self.pose
        dist_goal = np.linalg.norm(to_goal)

        if dist_goal < self.goal_tol:
            if not self._reached:
                self._reached = True
                self.get_logger().info("Goal reached.")
                self._publish_stats(done=True)
            self._publish_velocity(np.zeros(3))
            return

        # attractive velocity in body FLU frame
        goal_flu = self._enu_to_flu(to_goal)
        v_att = self.k_att * goal_flu
        if np.linalg.norm(v_att) > self.v_max:
            v_att = v_att / np.linalg.norm(v_att) * self.v_max

        # repulsive velocity from obstacle points (body FLU)
        v_rep = np.zeros(3)
        if self.obstacles_flu is not None and len(self.obstacles_flu):
            d = np.linalg.norm(self.obstacles_flu, axis=1)
            near = (d < self.d0) & (d > 1e-2)
            if near.any():
                pts = self.obstacles_flu[near]
                dd = d[near]
                # APF repulsion: eta (1/d - 1/d0) / d^2 along -point_dir
                mag = self.k_rep * (1.0 / dd - 1.0 / self.d0) / (dd ** 2)
                dirs = -pts / dd[:, None]
                v_rep = (dirs * mag[:, None]).sum(axis=0)

        v_flu = v_att + v_rep
        speed = np.linalg.norm(v_flu)
        if speed > self.v_max:
            v_flu = v_flu / speed * self.v_max

        # body FLU -> local ENU (yaw rotation; z stays up)
        v_enu = self._flu_to_enu(v_flu)
        self._publish_velocity(v_enu)
        self._publish_markers(v_enu)

        if self.auto_arm and MAVROS_OK:
            self._ensure_offboard_and_armed()

        self._publish_stats(done=False)

    # ── frame helpers ─────────────────────────────────────────────────────────
    def _enu_to_flu(self, v_enu):
        c, s = math.cos(-self.yaw), math.sin(-self.yaw)
        return np.array([c * v_enu[0] - s * v_enu[1], s * v_enu[0] + c * v_enu[1], v_enu[2]])

    def _flu_to_enu(self, v_flu):
        c, s = math.cos(self.yaw), math.sin(self.yaw)
        return np.array([c * v_flu[0] - s * v_flu[1], s * v_flu[0] + c * v_flu[1], v_flu[2]])

    # ── outputs ───────────────────────────────────────────────────────────────
    def _publish_velocity(self, v_enu):
        if self.vel_pub is None:
            return
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"
        msg.twist.linear.x = float(v_enu[0])
        msg.twist.linear.y = float(v_enu[1])
        msg.twist.linear.z = float(v_enu[2])
        self.vel_pub.publish(msg)

    def _publish_stats(self, done):
        straight = np.linalg.norm(self.goal - self._start_pos) if self._start_pos is not None else 0.0
        eff = straight / self._traveled if self._traveled > 1e-3 else 1.0
        msg = String()
        msg.data = (f"reached={done} traveled_m={self._traveled:.1f} straight_m={straight:.1f} "
                    f"path_efficiency={eff:.2f} min_obstacle_dist_m="
                    f"{(self._min_obs_dist if np.isfinite(self._min_obs_dist) else -1):.2f}")
        self.stats_pub.publish(msg)

    def _publish_markers(self, v_enu):
        arr = MarkerArray()
        stamp = self.get_clock().now().to_msg()
        goal = Marker()
        goal.header.frame_id = "map"; goal.header.stamp = stamp
        goal.ns = "goal"; goal.id = 0; goal.type = Marker.SPHERE; goal.action = Marker.ADD
        goal.pose.position.x, goal.pose.position.y, goal.pose.position.z = map(float, self.goal)
        goal.pose.orientation.w = 1.0
        goal.scale.x = goal.scale.y = goal.scale.z = 0.7
        goal.color = ColorRGBA(r=1.0, g=0.85, b=0.1, a=1.0)
        arr.markers.append(goal)
        if self.pose is not None:
            v = Marker()
            v.header.frame_id = "map"; v.header.stamp = stamp
            v.ns = "cmd_vel"; v.id = 1; v.type = Marker.ARROW; v.action = Marker.ADD
            v.scale.x = 0.1; v.scale.y = 0.2; v.scale.z = 0.2
            v.color = ColorRGBA(r=0.1, g=0.9, b=1.0, a=1.0)
            p0 = Point(x=float(self.pose[0]), y=float(self.pose[1]), z=float(self.pose[2]))
            p1 = Point(x=float(self.pose[0] + v_enu[0]), y=float(self.pose[1] + v_enu[1]),
                       z=float(self.pose[2] + v_enu[2]))
            v.points = [p0, p1]
            arr.markers.append(v)
        self.marker_pub.publish(arr)

    # ── offboard/arm ──────────────────────────────────────────────────────────
    def _ensure_offboard_and_armed(self):
        now = self.get_clock().now()
        if (now - self._last_req).nanoseconds < 2e9 or not self.state.connected:
            return
        if self.state.mode != "OFFBOARD":
            if self.mode_cli.wait_for_service(timeout_sec=0.1):
                req = SetMode.Request(); req.custom_mode = "OFFBOARD"
                self.mode_cli.call_async(req)
            self._last_req = now
        elif not self.state.armed:
            if self.arm_cli.wait_for_service(timeout_sec=0.1):
                req = CommandBool.Request(); req.value = True
                self.arm_cli.call_async(req)
            self._last_req = now

    @staticmethod
    def _read_xyz(msg: PointCloud2):
        if msg.point_step < 12:
            return None
        n = msg.width * msg.height
        if n == 0:
            return None
        buf = np.frombuffer(msg.data, dtype=np.uint8).reshape(n, msg.point_step)
        xyz = np.frombuffer(buf[:, 0:12].tobytes(), dtype=np.float32).reshape(n, 3)
        return xyz[np.isfinite(xyz).all(axis=1)]


def main(args=None):
    rclpy.init(args=args)
    node = LocalPlannerNode()
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
