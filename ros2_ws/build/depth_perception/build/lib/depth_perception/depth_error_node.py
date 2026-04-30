#!/usr/bin/env python3
"""
Depth Error Analysis Node  (Optional deliverable)
--------------------------------------------------
Compares estimated depth with Gazebo ground-truth depth and computes:
  - MAE  (Mean Absolute Error)
  - RMSE (Root Mean Squared Error)
  - Error distribution binned by distance

Subscribes to:
  - /camera/depth/image          (Gazebo ground-truth depth, float32 m)
  - /camera/depth/image_estimated (monocular estimated depth, float32 m)
    [If you only have GT depth from Gazebo, this node becomes a pass-through stats node]

Publishes:
  - /depth/error_stats  (String) — JSON-formatted metrics per frame

Also saves a CSV log to /tmp/depth_error_log.csv for offline plotting.
"""

import csv
import json
import time
from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from message_filters import ApproximateTimeSynchronizer, Subscriber

from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge


class DepthErrorNode(Node):

    def __init__(self):
        super().__init__("depth_error_node")

        self.declare_parameter("gt_topic",  "/camera/depth/image")
        self.declare_parameter("est_topic", "/camera/depth/image_estimated")
        self.declare_parameter("max_depth", 10.0)
        self.declare_parameter("n_bins",    10)
        self.declare_parameter("log_csv",   "/tmp/depth_error_log.csv")

        p = lambda n: self.get_parameter(n).value
        self.max_depth = p("max_depth")
        self.n_bins    = p("n_bins")
        log_path       = p("log_csv")

        self.bridge    = CvBridge()
        self._frame    = 0

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )

        self.gt_sub  = Subscriber(self, Image, p("gt_topic"),  qos_profile=qos)
        self.est_sub = Subscriber(self, Image, p("est_topic"), qos_profile=qos)

        self.sync = ApproximateTimeSynchronizer(
            [self.gt_sub, self.est_sub], queue_size=10, slop=0.15
        )
        self.sync.registerCallback(self._cb)

        self.pub = self.create_publisher(String, "/depth/error_stats", 10)

        # CSV log
        self._csv_path = Path(log_path)
        self._csv_file = self._csv_path.open("w", newline="")
        self._csv_writer = csv.writer(self._csv_file)
        self._csv_writer.writerow(["frame", "timestamp", "n_valid", "mae", "rmse",
                                   "mean_gt_depth", "mean_est_depth"])

        self.get_logger().info(
            f"DepthErrorNode ready. Comparing {p('gt_topic')} vs {p('est_topic')}"
        )
        self.get_logger().info(f"CSV log → {log_path}")

    def _cb(self, gt_msg: Image, est_msg: Image):
        try:
            gt  = self.bridge.imgmsg_to_cv2(gt_msg,  desired_encoding="passthrough").astype(np.float32)
            est = self.bridge.imgmsg_to_cv2(est_msg, desired_encoding="passthrough").astype(np.float32)
        except Exception as e:
            self.get_logger().error(f"CvBridge: {e}")
            return

        # Align shapes (crop to smaller)
        h = min(gt.shape[0], est.shape[0])
        w = min(gt.shape[1], est.shape[1])
        gt  = gt[:h, :w]
        est = est[:h, :w]

        valid = (
            (gt  > 0.1) & (gt  < self.max_depth) & np.isfinite(gt) &
            (est > 0.1) & (est < self.max_depth) & np.isfinite(est)
        )

        if valid.sum() < 100:
            return

        gt_v  = gt[valid]
        est_v = est[valid]
        err   = np.abs(gt_v - est_v)

        mae  = float(err.mean())
        rmse = float(np.sqrt((err ** 2).mean()))

        # Bin errors by ground-truth distance
        bin_edges = np.linspace(0.1, self.max_depth, self.n_bins + 1)
        bin_mae   = []
        for i in range(self.n_bins):
            mask = (gt_v >= bin_edges[i]) & (gt_v < bin_edges[i + 1])
            if mask.any():
                bin_mae.append(float(err[mask].mean()))
            else:
                bin_mae.append(None)

        self._frame += 1
        ts = gt_msg.header.stamp.sec + gt_msg.header.stamp.nanosec * 1e-9

        # Publish stats
        stats = {
            "frame":          self._frame,
            "mae_m":          round(mae, 4),
            "rmse_m":         round(rmse, 4),
            "mean_gt_depth":  round(float(gt_v.mean()), 3),
            "mean_est_depth": round(float(est_v.mean()), 3),
            "n_valid":        int(valid.sum()),
            "bin_edges_m":    [round(e, 2) for e in bin_edges.tolist()],
            "bin_mae_m":      [round(v, 4) if v is not None else None for v in bin_mae],
        }
        msg = String()
        msg.data = json.dumps(stats)
        self.pub.publish(msg)

        # Write CSV
        self._csv_writer.writerow([
            self._frame, round(ts, 3), int(valid.sum()),
            round(mae, 4), round(rmse, 4),
            round(float(gt_v.mean()), 3), round(float(est_v.mean()), 3),
        ])
        self._csv_file.flush()

        if self._frame % 30 == 0:
            self.get_logger().info(
                f"[Frame {self._frame}] MAE={mae*100:.1f}cm  RMSE={rmse*100:.1f}cm  "
                f"n={valid.sum()}"
            )

    def destroy_node(self):
        self._csv_file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DepthErrorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
