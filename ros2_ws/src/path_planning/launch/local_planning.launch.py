"""
Aufgabe 2 - Local planner (obstacle avoidance) launch.

Starts:
  - local_planner_node (Artificial Potential Fields)
  - static TF world -> map
  - RViz2

Requires the Task 2 depth pipeline to be running so /point_cloud/obstacles is
available (ros2 launch depth_perception depth_perception.launch.py), plus PX4
SITL + MAVROS for the velocity setpoints to take effect.
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory("path_planning")
    rviz_cfg = os.path.join(pkg, "rviz", "path_planning.rviz")

    goal = DeclareLaunchArgument("goal", default_value="[20.0, 0.0, 3.0]")

    static_tf = Node(
        package="tf2_ros", executable="static_transform_publisher", name="map_static_tf",
        arguments=["0", "0", "0", "0", "0", "0", "world", "map"], output="screen")

    local = Node(
        package="path_planning", executable="local_planner_node", name="local_planner_node",
        parameters=[{"goal": LaunchConfiguration("goal")}], output="screen")

    rviz = Node(package="rviz2", executable="rviz2", name="rviz2",
                arguments=["-d", rviz_cfg], output="screen")

    return LaunchDescription([goal, static_tf, local, rviz])
