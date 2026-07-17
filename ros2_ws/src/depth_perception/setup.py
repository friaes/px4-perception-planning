from glob import glob

from setuptools import find_packages, setup

package_name = "depth_perception"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.py")),
        (f"share/{package_name}/rviz", glob("rviz/*.rviz")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="student",
    maintainer_email="student@example.com",
    description="ROS2 depth perception utilities for PX4 SITL camera streams",
    license="MIT",
    entry_points={
        "console_scripts": [
            "point_cloud_node = depth_perception.point_cloud_node:main"
        ],
    },
)