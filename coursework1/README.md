# ROS 2 Coursework 1: Beta Pilot Robot Control

This repository contains a ROS 2 workspace designed for the **Coursework 1 (Task 2)** project. The project implements a differential drive robot simulation with a dedicated controller that performs a sequential rotation and translation maneuver.

## 🚀 Project Overview

The system consists of several nodes communicating via custom topics and services to control a robot's movement based on specific physical parameters.

### Key Logic:
1.  **Rotation Phase**: The robot rotates in place until it reachers a target heading of **124.0°**.
2.  **Translation Phase**: After completing the rotation, the robot moves forward for a total distance of **1.0 meter**.
3.  **Completion**: Once the target distance is achieved, the controller stops the robot and turns it off using a service call.

---

## 📂 Repository Structure

*   `sfr_coursework1_interface_package`: Defines custom communication interfaces.
    *   **Messages**: `TaskSpacePose.msg`, `WheelAngularVelocities.msg`.
    *   **Services**: `TurnRobotOn.srv`, `TurnRobotOff.srv`.
*   `beta_pilot_pkg`: Contains the `beta_pilot_node` which simulates the robot's physical movement.
*   `beta_pilot_controller_pkg`: Contains the `beta_pilot_controller_node` which implements the control logic.
*   `beta_pilot_launch_pkg`: Provides launch files to orchestrate the nodes.

---

## 🛠️ Installation & Setup

### Prerequisites
*   ROS 2 (Humble/Jazzy/Rolling) installed on Linux.
*   `colcon` build tool.

### Hardware Parameters
The robot uses the following physical constants:
*   **Wheel Radius ($r$):** 0.09 m
*   **Wheel Separation ($l$):** 0.28 m
*   **Update Rate ($T$):** 0.1 s (10 Hz)
*   **Speed Limit:** Linear velocity is capped at **0.1 m/s**.

### Building the Workspace
From the root of the workspace (`coursework1` folder):

```bash
# Remove old build artifacts if necessary
rm -rf build/ install/ log/

# Build the workspace
colcon build --symlink-install
```

---

## 🚦 Running the Code

To run the full simulation (Robot + Controller):

```bash
# Source the install directory
source install/setup.bash

# Launch both nodes
ros2 launch beta_pilot_launch_pkg beta_pilot_controller_launch.py
```

### Alternative: Launching Individually
If you want to run the robot node only:
```bash
ros2 run beta_pilot_pkg beta_pilot_node
```

And in another terminal, run the controller:
```bash
ros2 run beta_pilot_controller_pkg beta_pilot_controller_node
```

---

## 📡 Interfaces

### Topics
*   `robot/task_space_pose` ([`TaskSpacePose`]): Broadcasts the current $(x, y, \phi)$ position of the robot.
*   `robot/wheel_angular_velocities` ([`WheelAngularVelocities`]): Receives rotation speed commands for the left and right wheels.

### Services
*   `robot/turn_robot_on` ([`TurnRobotOn`]): Enables robot movement.
*   `robot/turn_robot_off` ([`TurnRobotOff`]): Disables robot movement and resets velocities.

---

## 📝 Configuration
*   **Target Angle:** 124.0 degrees (configured in `beta_pilot_controller_node.py`).
*   **Target Distance:** 1.0 meter (configured in `beta_pilot_controller_node.py`).
