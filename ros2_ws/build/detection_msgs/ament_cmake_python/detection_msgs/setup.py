from setuptools import find_packages
from setuptools import setup

setup(
    name='detection_msgs',
    version='0.0.1',
    packages=find_packages(
        include=('detection_msgs', 'detection_msgs.*')),
)
