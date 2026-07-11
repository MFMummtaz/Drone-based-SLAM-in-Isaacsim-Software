# 🛸 VSLAM Autonomous UAV Simulation Stack

<p align="center">
  <img src="./images/simulation_snapshot.png" width="31%" alt="1"/>
  <img src="./images/drone_USD.png" width="31%" alt="2"/>
  <img src="./images/3d_map.png" width="31%" alt="3"/>
</p>


An advanced, GPU-accelerated autonomous UAV simulation environment for **GPS-denied navigation**. This repository bridges **NVIDIA Isaac Sim**, **Pegasus Simulator**, and **PX4-Autopilot** with hardware-accelerated **NVIDIA Isaac ROS Visual SLAM** for high-fidelity simulation and perception testing.

---

## 💻 System Requirements

Before you begin, ensure your workstation meets the following bare-minimum specifications:

| Component | Minimum Requirement |
| :--- | :--- |
| **Operating System** | Ubuntu 22.04 LTS |
| **CPU** | Intel Core i7 (7th Gen) / AMD Ryzen 5 or better |
| **RAM** | 32 GB |
| **Storage** | 50 GB SSD available space |
| **GPU** | NVIDIA GeForce RTX 4080 (Recommended) |
| **GPU Driver** | NVIDIA Driver v580+ |

---

## 📦 Prerequisites & Installation

### 1. Core Core Docker Setup
Install Docker and complete the [Docker Linux Post-Installation Steps](https://docs.docker.com/engine/install/linux-postinstall/) to manage containers without `sudo`.

Verify your installation:
```bash
docker run hello-world
```

### 2. Clone This Repository
Clone the core simulation packages into your local workspace:
```bash
git clone (https://github.com/bandofpv/VSLAM-UAV)
```

### 3. NVIDIA Container Toolkit
Install the NVIDIA Container Toolkit to enable GPU acceleration inside your Docker containers. (https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### 4. Simulator Suite Setup
- NVIDIA Isaac Sim: Install Isaac Sim (Version 5.1.0) along with its structural assets following the official Isaac Sim Installation Guide. (https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/requirements.html)
- Pegasus Simulator: Clone and build the Pegasus Simulator extension.
- Cross-linking: Configure the connection layer between Isaac Sim and Pegasus Simulator. (https://github.com/PegasusSimulator/PegasusSimulator)
- Robot Asset Injection: Copy the modified custom asset file Iris_VSLAM.usd included in this repository to your local directory layout:
```bash
cp Iris_VSLAM.usd /home/mummtaz/PegasusSimulator/extensions/pegasus.simulator/pegasus/simulator/assets/Robots/
```

### 5. Autopilot & GCS Setup
- Clone and build the PX4-Autopilot firmware ecosystem. (https://github.com/PX4/PX4-Autopilot.git)
- Establish the hardware-in-the-loop connection profile between Isaac Sim and the PX4-Autopilot framework.
- Download and install the QGroundControl application.

### 6. NVIDIA Isaac ROS Architecture
Install NVIDIA Isaac ROS Core Components. (https://nvidia-isaac-ros.github.io/getting_started/index.html) 
- In this project we used Segmentation part for segmenting Human-object inside of the simulation environment

## 🛠️ Build Phase (Crucial & Tricky)
Build the dedicated VSLAM local tracking container image by executing the following compilation routine:
```bash
cd ~/VSLAM-UAV/docker/sim
./run_docker.sh
```

## 🚀 Runtime Execution & Simulation Launch
To launch the full pipeline, orchestrate your execution using 4 independent terminal sessions:
- 🖥️ Terminal 1: Ground Control Station
Open the QGroundControl interface to track telemetry and missions:
```bash
# Launch QGroundControl executable
./QGroundControl.AppImage
```

- 🖥️ Terminal 2: VSLAM UAV Sim & MAVROS Bridge
Initialize the primary UAV simulation container environment and kick off the MAVROS communication layer:
```bash
cd ~/VSLAM-UAV/docker/sim
./run_docker.sh

# Inside the running docker container:
cd ~/VSLAM-UAV/sim
ros2 launch mavrospy.launch.py
```

- 🖥️ Terminal 3: Isaac ROS VSLAM Engine
Spin up the development environment container workspace and boot up the visual odometry nodes:
```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common
./scripts/run_dev.sh -b

# Inside the running developer container:
cd ${ISAAC_ROS_WS}/VSLAM-UAV/sim
ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam_isaac_sim.launch.py
```

- 🖥️ Terminal 4: Data Visualization (RViz2)
Spin up the visualization environment to view mapping landmarks and estimated trajectory coordinates:
```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common
./scripts/run_dev.sh

# Inside the running container:
rviz2 -d ${ISAAC_ROS_WS}/VSLAM-UAV/sim/isaac_sim.cfg.rviz
```

## 🏁 Final Step
Launch Isaac Sim locally and configure the active backend engine inside PegasusSimulator to map directly to PX4 utilizing the newly registered VSLAM-Drone vehicle definition.





