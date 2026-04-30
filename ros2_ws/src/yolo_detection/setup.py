from setuptools import setup, find_packages
import os
from glob import glob

package_name = "yolo_detection"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="student",
    maintainer_email="student@example.com",
    description="ROS2 YOLO object detection node for PX4 SITL",
    license="MIT",
    entry_points={
        "console_scripts": [
            "yolo_node       = yolo_detection.yolo_node:main",
        ],
    },
)
