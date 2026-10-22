# Articubot One (ROS 2 Jazzy & Gazebo Harmonic)

A differential drive mobile robot simulation built for **ROS 2 Jazzy** using **Gazebo Harmonic (`ros_gz`)**.

## 🎥 Simulation Demo

https://github.com/user-attachments/assets/Result.mp4

> **Demo video available at [`docs/Result.mp4`](docs/Result.mp4)**: Shows the robot navigating through the construction cone & barrel obstacle course in Gazebo Harmonic with zero-lag teleoperation.

---

## 🚀 Features

- **ROS 2 Jazzy Jalisco** & **Gazebo Harmonic (gz-sim)** native compatibility.
- **Gazebo DiffDrive Plugin** with bridged `/cmd_vel`, `/odom`, `/clock`, and `/tf` topics via `ros_gz_bridge`.
- **Responsive Teleoperation Node** (`smooth_teleop.py`) providing instantaneous, non-blocking direct velocity commands (WASD controls).
- Fully modeled obstacles world with construction barrels and cones.

---

## 📦 Installation & Setup

```bash
# Clone the repository into your ROS 2 workspace
cd ~/dev_ws/src
git clone https://github.com/samstromer1990-crypto/articubot_one.git

# Install dependencies
sudo apt update
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge

# Build the workspace
cd ~/dev_ws
colcon build --symlink-install --packages-select articubot_one
source install/setup.bash
```

---

## 🎮 Running the Simulation

### 1. Launch Gazebo Simulation
```bash
ros2 launch articubot_one launch_sim.launch.py
```

### 2. Drive the Robot (Keyboard Teleop)
In a second terminal:
```bash
ros2 run articubot_one smooth_teleop.py
```

#### Controls:
- **`W`** : Drive Forward
- **`S`** : Drive Backward
- **`A`** : Turn Left
- **`D`** : Turn Right
- **`Space`** / **`K`** : Stop
- **`+`** / **`-`** : Increase / Decrease speed
