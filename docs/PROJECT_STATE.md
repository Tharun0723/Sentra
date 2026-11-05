# SENTRA — Latest Development Checkpoint
## 5 November 2026

### Completed Milestones

#### Robot simulation and movement
- SENTRA successfully spawned in Gazebo Harmonic.
- Differential drive controllers configured and activated.
- Forward, reverse and in-place rotation tested successfully.
- Reduced fixed caster friction to allow in-place rotation.

#### LiDAR integration
- Added Gazebo Sensors system plugin to empty.sdf.
- Added a 2D GPU LiDAR sensor to lidar_link.
- Configured 360-degree field of view.
- Configured 720 horizontal samples.
- Configured 0.12 m minimum and 12 m maximum range.
- Verified Gazebo publishes /scan as gz.msgs.LaserScan.
- Created Gazebo-to-ROS 2 bridge.
- Verified ROS 2 publishes /scan as sensor_msgs/msg/LaserScan.
- Verified approximately 6.8 Hz scan frequency in the current WSL environment.
- Corrected ROS scan frame using override_frame_id:=lidar_link.
- Verified base_link to lidar_link transform:
  Translation: [-0.080, 0.000, 0.615]

#### RViz visualization
- Successfully displayed SENTRA RobotModel and TF.
- Added LaserScan display on /scan.
- LaserScan status verified as OK.
- Obstacle detection in a non-empty world is still pending.

#### WSL graphics
- Identified software rendering through llvmpipe.
- Enabled hardware-accelerated OpenGL using:
  GALLIUM_DRIVER=d3d12
  MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
- Verified NVIDIA Quadro P3200 hardware acceleration.
- RViz is now responsive.

### Current Environment
- Windows 11
- WSL2, Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic 8.15.0
- RViz2
- NVIDIA Quadro P3200
- Workspace: ~/sentra_ws

### Git
- Branch: main
- Previous verified commit: 61a0028
- Current changes: LiDAR integration, Gazebo Sensors plugin and RViz configuration.
- GitHub push for this checkpoint: Pending.

### Next Milestones
1. Add a test obstacle in Gazebo.
2. Verify LiDAR obstacle detection and scan points in RViz.
3. Design the custom industrial factory Gazebo world.
4. Integrate SLAM Toolbox.
5. Generate and save SENTRA's 2D occupancy-grid map.
6. Integrate Nav2 for autonomous navigation.

### Important Notes
- The current empty world produces mostly infinite LiDAR ranges.
- Do not consider obstacle detection validated until tested with objects.
- ROS 2 bridge is currently launched manually in a separate terminal.
- RViz should be launched with NVIDIA D3D12 environment variables.
