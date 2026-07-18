"""
Aufgabe 1 - Global planner launch.

Starts:
  - global_planner_node (A* / RRT on a 3D voxel grid) with params/scenario.yaml
  - static TF world -> map (so RViz has a frame)
  - RViz2 with the path-planning layout
  - (optional) mission_executor_node to fly the path on PX4  [execute:=true]

Run PX4 SITL (make px4_sitl gz_x500_depth) + MAVROS separately before using
execute:=true.
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory("path_planning")
    params = os.path.join(pkg, "params", "scenario.yaml")
    rviz_cfg = os.path.join(pkg, "rviz", "path_planning.rviz")

    algorithm = DeclareLaunchArgument("algorithm", default_value="astar")
    execute = DeclareLaunchArgument("execute", default_value="false")
    exec_mode = DeclareLaunchArgument("exec_mode", default_value="offboard")  # offboard | mission

    static_tf = Node(
        package="tf2_ros", executable="static_transform_publisher", name="map_static_tf",
        arguments=["0", "0", "0", "0", "0", "0", "world", "map"], output="screen")

    planner = Node(
        package="path_planning", executable="global_planner_node", name="global_planner_node",
        parameters=[params, {"algorithm": LaunchConfiguration("algorithm")}],
        output="screen")

    rviz = Node(package="rviz2", executable="rviz2", name="rviz2",
                arguments=["-d", rviz_cfg], output="screen")

    executor = Node(
        package="path_planning", executable="mission_executor_node", name="mission_executor_node",
        condition=IfCondition(LaunchConfiguration("execute")),
        parameters=[{"mode": LaunchConfiguration("exec_mode")}],
        output="screen")

    return LaunchDescription([algorithm, execute, exec_mode, static_tf, planner, rviz, executor])
