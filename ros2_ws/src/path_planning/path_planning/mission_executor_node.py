#!/usr/bin/env python3
import math

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

try:
    from mavros_msgs.msg import State
    from mavros_msgs.srv import CommandBool, SetMode, CommandTOL, WaypointPush
    from mavros_msgs.msg import Waypoint
    from sensor_msgs.msg import NavSatFix
    MAVROS_OK = True
except Exception:                      # pragma: no cover
    MAVROS_OK = False


class MissionExecutorNode(Node):

    def __init__(self):
        super().__init__("mission_executor_node")
        self.declare_parameter("mode", "offboard")
        self.declare_parameter("accept_radius", 0.6)
        self.declare_parameter("takeoff_alt", 2.0)
        self.declare_parameter("auto_arm", True)
        self.declare_parameter("setpoint_rate", 20.0)
        self.declare_parameter("yaw_smoothing", 0.05)   # 0=frozen heading, 1=instant snap

        g = lambda n: self.get_parameter(n).value
        self.mode = g("mode")
        self.accept_radius = g("accept_radius")
        self.takeoff_alt = g("takeoff_alt")
        self.auto_arm = g("auto_arm")
        rate = g("setpoint_rate")
        self.yaw_smoothing = float(g("yaw_smoothing"))

        if not MAVROS_OK:
            self.get_logger().error("mavros_msgs not available - cannot talk to PX4. Is MAVROS installed/running?")
            return

        self.path = []          # list of np.array([x,y,z])
        self.wp_idx = 0
        self.state = State()
        self.pose = None
        self.home_fix = None
        self._mission_uploaded = False
        self._arm_attempts = 0
        self._yaw_cmd = None
        self._last_req = self.get_clock().now()

        latched = QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE,
                             durability=DurabilityPolicy.TRANSIENT_LOCAL,
                             history=HistoryPolicy.KEEP_LAST)
        sensor = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT,
                            history=HistoryPolicy.KEEP_LAST)

        self.create_subscription(Path, "/planner/path", self._path_cb, latched)
        self.create_subscription(State, "/mavros/state", self._state_cb, 10)
        self.create_subscription(PoseStamped, "/mavros/local_position/pose", self._pose_cb, sensor)
        self.create_subscription(NavSatFix, "/mavros/global_position/global", self._fix_cb, sensor)

        self.sp_pub = self.create_publisher(PoseStamped, "/mavros/setpoint_position/local", 10)

        self.arm_cli = self.create_client(CommandBool, "/mavros/cmd/arming")
        self.mode_cli = self.create_client(SetMode, "/mavros/set_mode")
        self.push_cli = self.create_client(WaypointPush, "/mavros/mission/push")

        self.create_timer(1.0 / rate, self._tick)
        self.get_logger().info(f"MissionExecutorNode ready (mode={self.mode}).")

    # ── callbacks ─────────────────────────────────────────────────────────────
    def _path_cb(self, msg: Path):
        self.path = [np.array([p.pose.position.x, p.pose.position.y, p.pose.position.z]) for p in msg.poses]
        self.wp_idx = 0
        self._mission_uploaded = False
        self.get_logger().info(f"Received path with {len(self.path)} waypoints.")

    def _state_cb(self, msg):
        self.state = msg

    def _pose_cb(self, msg):
        self.pose = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])

    def _fix_cb(self, msg):
        if self.home_fix is None and msg.status.status >= 0:
            self.home_fix = (msg.latitude, msg.longitude, msg.altitude)

    # ── main loop ─────────────────────────────────────────────────────────────
    def _tick(self):
        if not MAVROS_OK or not self.path:
            return
        if self.mode == "mission":
            self._tick_mission()
        else:
            self._tick_offboard()

    # ---- offboard ----
    def _tick_offboard(self):
        target = self._current_target()

        sp = PoseStamped()
        sp.header.frame_id = "map"
        sp.header.stamp = self.get_clock().now().to_msg()
        sp.pose.position.x, sp.pose.position.y, sp.pose.position.z = map(float, target)

        # Yaw setpoint: point the nose along the current PATH SEGMENT rather than
        # at the instantaneous vector to the target. The latter shrinks and swings
        # wildly as the vehicle closes in, which makes the drone fly sideways and
        # snap its heading at each waypoint. Segment direction is stable, and we
        # low-pass it so the turn is smooth.
        yaw = self._segment_yaw()
        if yaw is not None:
            if self._yaw_cmd is None:
                self._yaw_cmd = yaw
            else:
                # shortest-angle smoothing
                err = math.atan2(math.sin(yaw - self._yaw_cmd), math.cos(yaw - self._yaw_cmd))
                self._yaw_cmd += self.yaw_smoothing * err
        if self._yaw_cmd is not None:
            sp.pose.orientation.z = math.sin(self._yaw_cmd / 2)
            sp.pose.orientation.w = math.cos(self._yaw_cmd / 2)
        else:
            sp.pose.orientation.w = 1.0
        self.sp_pub.publish(sp)          # must stream continuously for OFFBOARD

        # advance waypoint on proximity
        if self.pose is not None and self.wp_idx < len(self.path):
            if np.linalg.norm(self.pose - self.path[self.wp_idx]) < self.accept_radius:
                if self.wp_idx < len(self.path) - 1:
                    self.wp_idx += 1
                    self.get_logger().info(f"Reached waypoint {self.wp_idx}/{len(self.path) - 1}")

        if self.auto_arm:
            self._ensure_offboard_and_armed()

    def _segment_yaw(self):
        """Heading along the active path segment (previous waypoint -> current)."""
        if not self.path:
            return None
        i = min(self.wp_idx, len(self.path) - 1)
        tgt = self.path[i]
        # segment start: previous waypoint if we have one, else current position
        if i > 0:
            src = self.path[i - 1]
        elif self.pose is not None:
            src = self.pose
        else:
            return None
        dx, dy = tgt[0] - src[0], tgt[1] - src[1]
        if dx * dx + dy * dy < 0.25:      # segment is essentially vertical -> hold yaw
            return None
        return math.atan2(dy, dx)

    def _current_target(self):
        if self.wp_idx >= len(self.path):
            return self.path[-1]
        tgt = self.path[self.wp_idx].copy()
        # ensure we climb to takeoff_alt before chasing the first far waypoint
        if self.wp_idx == 0 and self.pose is not None and self.pose[2] < self.takeoff_alt - 0.3:
            tgt = self.pose.copy()
            tgt[2] = self.takeoff_alt
        return tgt

    def _ensure_offboard_and_armed(self):
        now = self.get_clock().now()
        if (now - self._last_req).nanoseconds < 2e9:   # throttle service calls to 0.5 Hz
            return
        if not self.state.connected:
            return
        if self.state.mode != "OFFBOARD":
            self._call_set_mode("OFFBOARD")
            self._last_req = now
        elif not self.state.armed:
            self._call_arm(True)
            self._arm_attempts += 1
            if self._arm_attempts == 12:
                self.get_logger().warn(
                    "Arming keeps being denied. This is almost always a PX4 preflight "
                    "failure, not a MAVROS problem - check the PX4 console for "
                    "'Preflight Fail' lines (missing accel/gyro/baro/compass means "
                    "Gazebo is not delivering sensor data; try HEADLESS=1).")
            self._last_req = now

    # ---- mission ----
    def _tick_mission(self):
        if self.home_fix is None:
            self.get_logger().warn("Waiting for GPS/home for mission upload...", throttle_duration_sec=5.0)
            return
        if not self._mission_uploaded:
            self._upload_mission()
            return
        if self.auto_arm and self.state.connected:
            now = self.get_clock().now()
            if (now - self._last_req).nanoseconds < 2e9:
                return
            if self.state.mode != "AUTO.MISSION":
                self._call_set_mode("AUTO.MISSION")
                self._last_req = now
            elif not self.state.armed:
                self._call_arm(True)
                self._last_req = now

    def _upload_mission(self):
        lat0, lon0, alt0 = self.home_fix
        wps = []
        for i, wp in enumerate(self.path):
            lat, lon = self._enu_to_geodetic(wp[0], wp[1], lat0, lon0)
            w = Waypoint()
            w.frame = 3                       # MAV_FRAME_GLOBAL_REL_ALT
            w.command = 16                    # NAV_WAYPOINT
            w.is_current = (i == 0)
            w.autocontinue = True
            w.param1 = 0.0                    # hold time
            w.param2 = self.accept_radius     # acceptance radius
            w.x_lat = lat
            w.y_long = lon
            w.z_alt = float(wp[2])            # relative altitude
            wps.append(w)

        if not self.push_cli.wait_for_service(timeout_sec=0.1):
            self.get_logger().warn("mission/push service not available yet...", throttle_duration_sec=5.0)
            return
        req = WaypointPush.Request()
        req.start_index = 0
        req.waypoints = wps
        fut = self.push_cli.call_async(req)
        fut.add_done_callback(self._on_push_done)
        self._mission_uploaded = True         # avoid re-spamming; reset on new path

    def _on_push_done(self, fut):
        try:
            res = fut.result()
            if res.success:
                self.get_logger().info(f"Mission uploaded: {res.wp_transfered} waypoints.")
            else:
                self.get_logger().error("Mission upload failed.")
                self._mission_uploaded = False
        except Exception as e:
            self.get_logger().error(f"Mission push error: {e}")
            self._mission_uploaded = False

    @staticmethod
    def _enu_to_geodetic(x_east, y_north, lat0_deg, lon0_deg):
        # equirectangular approximation around home (fine for a few hundred metres)
        R = 6378137.0
        lat0 = math.radians(lat0_deg)
        dlat = y_north / R
        dlon = x_east / (R * math.cos(lat0))
        return lat0_deg + math.degrees(dlat), lon0_deg + math.degrees(dlon)

    # ── service helpers ───────────────────────────────────────────────────────
    def _call_set_mode(self, mode):
        if self.mode_cli.wait_for_service(timeout_sec=0.1):
            req = SetMode.Request()
            req.custom_mode = mode
            self.mode_cli.call_async(req)
            self.get_logger().info(f"Requesting mode {mode}")

    def _call_arm(self, value):
        if self.arm_cli.wait_for_service(timeout_sec=0.1):
            req = CommandBool.Request()
            req.value = value
            self.arm_cli.call_async(req)
            self.get_logger().info(f"Requesting {'ARM' if value else 'DISARM'}")


def main(args=None):
    rclpy.init(args=args)
    node = MissionExecutorNode()
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