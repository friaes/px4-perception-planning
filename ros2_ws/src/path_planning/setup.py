from glob import glob

from setuptools import find_packages, setup

package_name = "path_planning"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.py")),
        (f"share/{package_name}/rviz", glob("rviz/*.rviz")),
        (f"share/{package_name}/params", glob("params/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="student",
    maintainer_email="student@example.com",
    description="Aufgabe 09: 3D global path planning (A*/RRT) and local obstacle avoidance (APF) for PX4 SITL",
    license="MIT",
    entry_points={
        "console_scripts": [
            "global_planner_node = path_planning.global_planner_node:main",
            "mission_executor_node = path_planning.mission_executor_node:main",
            "local_planner_node = path_planning.local_planner_node:main",
        ],
    },
)
