#!/usr/bin/env python3
import time
from collections import deque

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from detection_msgs.msg import Detection2D, Detection2DArray

from ultralytics import YOLO


class YoloDetectionNode(Node):
    def __init__(self):
        super().__init__("yolo_detection_node")

        # ── Parameters ────────────────────────────────────────────────────────
        self.declare_parameter("model", "yolov8n.pt")          # nano
        self.declare_parameter("confidence_threshold", 0.4)
        self.declare_parameter("image_topic", "/camera/color/image")
        self.declare_parameter("device", "cpu")                # "cpu" or "0" for GPU
        self.declare_parameter("fps_window", 30)               

        model_name  = self.get_parameter("model").value
        self.conf   = self.get_parameter("confidence_threshold").value
        img_topic   = self.get_parameter("image_topic").value
        device      = self.get_parameter("device").value
        fps_window  = self.get_parameter("fps_window").value

        # ── Load YOLO model ─────────────────────────────────────────────────────────
        self.get_logger().info(f"Loading YOLO model: {model_name} on device={device}")
        self.model = YOLO(model_name)
        self.model.to(device)
        self.get_logger().info("Model loaded successfully.")

        # ── CV Bridge ────────────────────────────────────────────────────────
        self.bridge = CvBridge()

        # ── QoS ─────────────────────────────────────────────────────
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # ── Subscriber ──────────────────────────────────────────────────────
        self.sub = self.create_subscription(
            Image, img_topic, self.image_callback, qos
        )
        self.get_logger().info(f"Subscribed to: {img_topic}")

        # ── Publishers ────────────────────────────────────────────────────────
        self.det_pub = self.create_publisher(Detection2DArray, "/detections", 10)
        self.img_pub = self.create_publisher(Image, "/perception/image_annotated", 10)

        # ── Performance tracking ──────────────────────────────────────────────
        self._frame_times: deque = deque(maxlen=fps_window)
        self._last_frame_time: float = time.time()
        self._frame_count = 0

    # ─────────────────────────────────────────────────────────────────────────
    def image_callback(self, msg: Image):
        t_start = time.time()

        # Convert ROS Image into OpenCV BGR
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error(f"CvBridge failed: {e}")
            return

        # ── YOLO Inference ──────────────────────────────────────────────
        t_infer_start = time.time()
        results = self.model.predict(frame, conf=self.conf, verbose=False)
        t_infer_end = time.time()
        inference_ms = (t_infer_end - t_infer_start) * 1000.0

        # ── Build Detection2DArray message ──────────────────────────────
        det_array = Detection2DArray()
        det_array.header = msg.header

        result = results[0]  # single image -> single result
        annotated_frame = frame.copy()  # Copy for annotation
        if result.boxes is not None:
            boxes      = result.boxes.xyxy.cpu().numpy()    # [N, 4]
            confs      = result.boxes.conf.cpu().numpy()    # [N]
            class_ids  = result.boxes.cls.cpu().numpy().astype(int)  # [N]

            for i in range(len(boxes)):
                det = Detection2D()
                det.x_min       = float(boxes[i][0])
                det.y_min       = float(boxes[i][1])
                det.x_max       = float(boxes[i][2])
                det.y_max       = float(boxes[i][3])
                det.confidence  = float(confs[i])
                det.class_id    = int(class_ids[i])
                det.class_name  = result.names[int(class_ids[i])]
                det_array.detections.append(det)

                # ── Draw annotation on frame ──────────────────────────────
                x_min, y_min, x_max, y_max = int(boxes[i][0]), int(boxes[i][1]), int(boxes[i][2]), int(boxes[i][3])
                conf = confs[i]
                class_name = result.names[int(class_ids[i])]
                label = f"{class_name} {conf:.2f}"

                # Draw bounding box (green)
                cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                # Draw label background and text
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                cv2.rectangle(annotated_frame, (x_min, y_min - text_size[1] - 4), (x_min + text_size[0], y_min), (0, 255, 0), -1)
                cv2.putText(annotated_frame, label, (x_min, y_min - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # ── FPS calculation ─────────────────────────────────────────────────────
        now = time.time()
        self._frame_times.append(now)
        if len(self._frame_times) >= 2:
            elapsed = self._frame_times[-1] - self._frame_times[0]
            fps = (len(self._frame_times) - 1) / elapsed if elapsed > 0 else 0.0
        else:
            fps = 0.0

        total_ms = (now - t_start) * 1000.0

        det_array.inference_latency_ms = float(inference_ms)
        det_array.total_latency_ms     = float(total_ms)
        det_array.fps                  = float(fps)

        self.det_pub.publish(det_array)

        # ── Publish annotated image ───────────────────────────────────────
        try:
            annotated_msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding="bgr8")
            annotated_msg.header = msg.header
            self.img_pub.publish(annotated_msg)
        except Exception as e:
            self.get_logger().error(f"Failed to publish annotated image: {e}")

        # ── Log every 30 frames ───────────────────────────────────────────────
        self._frame_count += 1
        if self._frame_count % 30 == 0:
            self.get_logger().info(
                f"[Frame {self._frame_count}] "
                f"Objects: {len(det_array.detections)} | "
                f"Inference: {inference_ms:.1f}ms | "
                f"Total: {total_ms:.1f}ms | "
                f"FPS: {fps:.1f}"
            )


# ─────────────────────────────────────────────────────────────────────────────
def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
