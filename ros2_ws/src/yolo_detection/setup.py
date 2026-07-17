from setuptools import setup, find_packages
from setuptools.command.develop import develop
import os
from glob import glob

package_name = "yolo_detection"


class ColconDevelopCommand(develop):
    """Keep compatibility with colcon's legacy develop --uninstall invocation."""

    user_options = develop.user_options + [
        ("uninstall", "u", "ignored compatibility option for colcon"),
    ]
    boolean_options = develop.boolean_options + ["uninstall"]

    def initialize_options(self):
        super().initialize_options()
        self.uninstall = False

    def run(self):
        # Newer setuptools dropped uninstall support in develop; colcon may still pass it.
        if self.uninstall:
            return
        super().run()

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
    cmdclass={"develop": ColconDevelopCommand},
    entry_points={
        "console_scripts": [
            "yolo_node       = yolo_detection.yolo_node:main",
        ],
    },
)
