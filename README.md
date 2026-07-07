# 🛸 VSLAM Autonomous UAV Simulation Stack

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
