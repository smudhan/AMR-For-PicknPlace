# AMR For Pick and Place 🤖

A ROS 2 Humble based Autonomous Mobile Robot (AMR) project developed from scratch for autonomous navigation and future warehouse pick-and-place applications.

The project includes a custom AMR robot model, Gazebo simulation, differential-drive control, LiDAR sensing, SLAM-based mapping, AMCL localization, and Nav2 autonomous navigation.

---

## 🚀 Project Overview

The goal of this project is to build a complete autonomous mobile base that can:

- Simulate a custom AMR in Gazebo
- Move using a differential-drive system
- Obtain wheel odometry through `ros2_control`
- Perceive the environment using a 2D LiDAR
- Build a map using SLAM Toolbox
- Localize itself using AMCL
- Plan collision-free paths using Nav2
- Navigate autonomously to a specified goal pose

  
<img width="1534" height="980" alt="image" src="https://github.com/user-attachments/assets/b36a05aa-1a38-4b76-bd3d-1e9a19ba5d53" />

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/8132142c-7cfa-426f-8623-00fc91734c13" />

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/af165f53-10a2-4f5a-950c-a43dfc208003" />



This mobile base is intended to serve as the navigation platform for a future **warehouse pick-and-place system**.

---

## 🏗️ Project Structure

```text
amr_description/
├── CMakeLists.txt
├── package.xml
│
├── config/
│   ├── amcl.yaml
│   ├── controllers.yaml
│   ├── nav2_params.yaml
│   └── slam_toolbox.yaml
│
├── launch/
│   ├── display.launch.py
│   ├── gazebo.launch.py
│   ├── localization.launch.py
│   ├── nav2.launch.py
│   └── slam.launch.py
│
├── map/
│   ├── map0/
│   │   ├── map.data
│   │   ├── map.pgm
│   │   ├── map.posegraph
│   │   └── map.yaml
│   │
│   └── map1/
│
├── meshes/
│   └── amr_project1_chassis.stl
│
├── rviz/
│
├── src/
│   └── teleop.py
│
├── urdf/
│   └── amr.urdf.xacro
│
└── worlds/
    └── empty.world
```
## 🚀 Running the Project

### 1. Requirements

Make sure the following are installed:

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic
- Nav2
- SLAM Toolbox
- `ros2_control`
- `gazebo_ros2_control`

Clone the repository:

```bash
mkdir amr_project1
mkdir ~/amr_project1/src
cd ~/amr_project1/src
git clone https://github.com/smudhan/AMR-For-PicknPlace.git

Build the workspace:
cd ~/amr_project1
colcon build --symlink-install
source install/setup.bash
```
2. Launch the Robot in Gazebo

   
<img width="1844" height="1173" alt="image" src="https://github.com/user-attachments/assets/49b1975c-5b50-402d-842c-0cba1a663fa7" />


Start the AMR simulation:

ros2 launch amr_description gazebo.launch.py

This launches the robot, Gazebo environment, LiDAR, ros2_control, and differential-drive controller.

3. Mapping with SLAM

To create a new map, start SLAM in another terminal:

source ~/amr_project1/install/setup.bash
ros2 launch amr_description slam.launch.py

Drive the robot around the environment using the included teleoperation node:

python3 ~/amr_project1/src/amr_description/src/teleop.py

After completing the map, save it using SLAM Toolbox.

4. Localization

After a map has been created, stop SLAM and launch localization:

ros2 launch amr_description localization.launch.py

Open RViz2 and set:

Fixed Frame: map

Use 2D Pose Estimate to initialize the robot's position on the map.

5. Autonomous Navigation with Nav2

With Gazebo and localization running, start Nav2 in another terminal:

source ~/amr_project1/install/setup.bash
ros2 launch amr_description nav2.launch.py

In RViz2, use 2D Goal Pose to select a destination.

Nav2 will then:

Goal
 ↓
Global Planner
 ↓
Global Costmap
 ↓
Local Controller
 ↓
Velocity Commands
 ↓
Differential Drive
 ↓
AMR

The robot will autonomously plan and navigate to the selected goal while using the LiDAR for obstacle detection.

📌 Launch File Summary
Launch file	            Purpose
display.launch.py	      Display the robot model in RViz
gazebo.launch.py	      Start Gazebo and the AMR simulation
slam.launch.py        	Build a map using SLAM Toolbox
localization.launch.py	Localize the robot using AMCL
nav2.launch.py	        Start autonomous navigation
