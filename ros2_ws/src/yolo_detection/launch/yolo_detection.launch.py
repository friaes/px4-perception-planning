from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # ── Launch arguments ──────────────────────────────────────────────────────
    model_arg = DeclareLaunchArgument(
        "model",
        default_value="yolov8n.pt",
        description="YOLO model weights file (yolov8n/s/m/l/x.pt or yolov11n.pt)"
    )
    conf_arg = DeclareLaunchArgument(
        "confidence_threshold",
        default_value="0.4",
        description="Detection confidence threshold"
    )
    device_arg = DeclareLaunchArgument(
        "device",
        default_value="cpu",
        description="Inference device: cpu or 0 (GPU)"
    )
    image_topic_arg = DeclareLaunchArgument(
        "image_topic",
        default_value="/camera/color/image",
        description="ROS2 image topic to subscribe to"
    )

    # ── ROS-Gazebo Bridge ─────────────────────────────────────────────────────
    # Maps the x500_depth camera stream from the active Gazebo world into ROS2.
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="camera_bridge",
        arguments=[
            # Camera image
            "/world/aufgabe1_fuel_world/model/x500_depth_0/link/camera_link/sensor/IMX214/image"
            "@sensor_msgs/msg/Image[gz.msgs.Image",
            # Camera info
            "/world/aufgabe1_fuel_world/model/x500_depth_0/link/camera_link/sensor/IMX214/camera_info"
            "@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
        ],
        remappings=[
            (
                "/world/aufgabe1_fuel_world/model/x500_depth_0/link/camera_link/sensor/IMX214/image",
                "/camera/color/image",
            ),
            (
                "/world/aufgabe1_fuel_world/model/x500_depth_0/link/camera_link/sensor/IMX214/camera_info",
                "/camera/color/camera_info",
            ),
        ],
        output="screen",
    )

    # ── YOLO detection node ───────────────────────────────────────────────────
    yolo_node = Node(
        package="yolo_detection",
        executable="yolo_node",
        name="yolo_detection_node",
        parameters=[{
            "model":                LaunchConfiguration("model"),
            "confidence_threshold": LaunchConfiguration("confidence_threshold"),
            "device":               LaunchConfiguration("device"),
            "image_topic":          LaunchConfiguration("image_topic"),
            "fps_window":           30,
        }],
        output="screen",
    )

    return LaunchDescription([
        model_arg,
        conf_arg,
        device_arg,
        image_topic_arg,
        ros_gz_bridge,
        yolo_node,
    ])
