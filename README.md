# Task 1 — Object Detection with YOLO

[fork](https://github.com/friaes/lecture8-perception)
ROS2 node that performs real-time YOLO object detection on the PX4 SITL camera stream.

## Step 1 — Build the Images

```bash
# Build everything
./build.sh --all

# Or build step by step
./build.sh --base  # ROS 2 + Gazebo
./build.sh --full  # PX4 Autopilot + MAVROS + NoVNC
```

## Step 2 — Start the container

```bash
docker compose up -d
# to close the container
docker compose down
```

## Step 3 — Build the ROS2 workspace

```bash
docker exec -it px4_sitl bash
cd /root/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Step 4 — Start the simulation (Terminal 1)

```bash
docker exec -it px4_sitl bash
cd /root/PX4-Autopilot
make px4_sitl gz_x500_depth
```

Access the GUI at: **http://localhost:6080/vnc.html** (password: `1234`)

Notes:
- The custom world file is mounted from `./worlds/aufgabe1_fuel_world.sdf`.

## Step 5 — Launch YOLO detection (Terminal 2)

```bash
docker exec -it px4_sitl bash
source /opt/ros/jazzy/setup.bash
source /root/ros2_ws/install/setup.bash

# Default: YOLOv8 nano (fastest)
ros2 launch yolo_detection yolo_detection.launch.py
```

The launch file automatically:
- Starts the ROS-Gazebo bridge (camera topic)
- Starts the YOLO inference node

## Step 6 — View the camera stream and detections

```bash
docker exec -it px4_sitl bash
source /opt/ros/jazzy/setup.bash
ros2 run rqt_image_view rqt_image_view /perception/image_annotated
```

![image](image_annotated.png)