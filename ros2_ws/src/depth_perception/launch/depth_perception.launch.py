from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path


def generate_launch_description():
    rviz_config = Path(get_package_share_directory("depth_perception")) / "rviz" / "depth_perception.rviz"

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="depth_perception_bridge",
        arguments=[
            "/world/aufgabe1_fuel_world/model/x500_depth_0/link/camera_link/sensor/IMX214/image@sensor_msgs/msg/Image@gz.msgs.Image",
            "/world/aufgabe1_fuel_world/model/x500_depth_0/link/camera_link/sensor/IMX214/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
            "/depth_camera@sensor_msgs/msg/Image@gz.msgs.Image",
            "/depth_camera/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",
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
            ("/depth_camera", "/camera/depth/image"),
            ("/depth_camera/points", "/camera/depth/points"),
        ],
        output="screen",
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", str(rviz_config)],
        output="screen",
    )

    point_cloud_node = Node(
        package="depth_perception",
        executable="point_cloud_node",
        name="point_cloud_node",
        output="screen",
    )

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="camera_link_static_tf",
        arguments=["0", "0", "0", "0", "0", "0", "world", "camera_link"],
        output="screen",
    )

    return LaunchDescription([
        static_tf,
        bridge,
        point_cloud_node,
        rviz,
    ])