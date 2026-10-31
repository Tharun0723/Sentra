# SENTRA system architecture

**Status:** Proposed design. Nothing in this file is implemented in `src/`.

This document exists so we can agree on subsystems, package boundaries, and ROS 2 interfaces **before** creating packages.

## 1. What “architecture” means here

A robotics system is easier to change when each package has:

- one clear job,
- known inputs and outputs,
- known dependencies,
- a reason it could not live in an existing package.

SENTRA will not start with nine packages because the project description lists nine conceptual subsystems. Several subsystems share a package until they become large enough to split.

## 2. Conceptual subsystems

```text
                    +---------------------------+
                    |  Inspection reporting     |
                    |  (files, later topics)    |
                    +------------^--------------+
                                 |
+-------------+   +--------------+---------------+   +------------------+
| Description |   | Mapping / localization / Nav2|   | Perception       |
| + Gazebo    |-->|  SLAM Toolbox, AMCL, Nav2    |   | camera, OpenCV,  |
| robot+world |   |  costmaps, waypoint follower |   | YOLO inference   |
+------+------+   +--------------^---------------+   +---------^--------+
       |                         |                             |
       | cmd_vel, sensors        | Nav2 actions                | images,
       | TF, clock               | feedback                    | detections
       v                         |                             |
+------+-------------------------+-----------------------------+--------+
|                 Mission manager (BehaviorTree.CPP)                    |
|  navigate -> inspect -> record -> next / return / recover / abort     |
+----------------------------------------------------------------------+
```

| Subsystem | Responsibility | First home (proposed package) |
|---|---|---|
| Robot description | URDF/Xacro, meshes, frames | `sentra_description` |
| Simulation | Worlds, spawn, `ros_gz` bridges | `sentra_gazebo` |
| Sensor processing | Mostly provided by Gazebo + bridges; extra filters only if needed | stay in sim / later small node |
| Mapping and localization | SLAM Toolbox, map server, AMCL, TF | `sentra_navigation` |
| Autonomous navigation | Nav2 params, waypoint poses | `sentra_navigation` |
| Computer vision | Image pipeline, detector node | `sentra_perception` |
| Mission management | Checkpoint list, mission state | `sentra_mission` |
| Behavior tree and recovery | BT XML, action/condition nodes | `sentra_mission` |
| Inspection reporting | JSON/YAML writer | `sentra_mission` |
| Monitoring and evaluation | Run logs, metrics scripts | `evaluation/` and later scripts; not a ROS package at the start |
| Bringup | Top-level launch files | `sentra_bringup` |

### Why these packages (and not more)

- **`sentra_description`** must be loadable in RViz without Gazebo. That is a standard split.
- **`sentra_gazebo`** holds worlds and bridge YAML that description should not own.
- **`sentra_navigation`** groups map, localization, and Nav2 config because they share frames, costmaps, and launch composition.
- **`sentra_perception`** is separate so vision dependencies (OpenCV, later PyTorch) do not burden the robot model.
- **`sentra_mission`** owns decision-making and reports. It should *call* Nav2 and perception, not embed their parameters.
- **`sentra_bringup`** is the only package a user should need to launch “the robot.”
- **No `sentra_msgs` yet.** Custom interfaces add build complexity. Use `sensor_msgs`, `nav_msgs`, `geometry_msgs`, `nav2_msgs`, `std_msgs`, and files until a field cannot be expressed that way.

These names are **candidates**. They will be created one at a time after approval.

## 3. Communication flow (target)

### 3.1 Coordinate frames (TF2)

Planned tree (2D mobile robot):

```text
map
 └── odom
      └── base_link
           ├── lidar_link   (or similar)
           ├── imu_link
           ├── camera_link
           ├── left_wheel_link
           └── right_wheel_link
```

| Frame | Role |
|---|---|
| `map` | World-fixed frame of the occupancy map. Localization publishes `map → odom`. |
| `odom` | Odometry frame. Continuous, can drift. Robot base is child of `odom`. |
| `base_link` | Robot body origin. Sensors are children of this (or of a chassis link). |

Do not add extra frames without a sensor or joint that needs them.

### 3.2 Standard topics and actions we intend to use

Names below are **standard ROS / Nav2 / sensor types**. Exact topic strings for SENTRA will be chosen when the robot is spawned and `ros2 topic list` is inspected. Do not treat placeholder names as already existing.

| Data | Typical message / interface | Producer (planned) | Consumer (planned) |
|---|---|---|---|
| Clock | `rosgraph_msgs/msg/Clock` | Gazebo via `ros_gz` | All nodes with `use_sim_time:=true` |
| TF | `tf2_msgs/msg/TFMessage` | `robot_state_publisher`, odom, AMCL | Nav2, RViz, mission |
| Joint states | `sensor_msgs/msg/JointState` | Gazebo / ros2_control | `robot_state_publisher` |
| Drive command | `geometry_msgs/msg/Twist` (or stamped equivalent required by the controller) | teleop or Nav2 | Gazebo diff-drive / ros2_control |
| LiDAR | `sensor_msgs/msg/LaserScan` | `ros_gz` bridge | SLAM Toolbox, Nav2 costmaps |
| IMU | `sensor_msgs/msg/Imu` | `ros_gz` bridge | optional fusion; later localization |
| RGB image | `sensor_msgs/msg/Image` | `ros_gz` / `ros_gz_image` | perception, RViz |
| Camera info | `sensor_msgs/msg/CameraInfo` | bridge | perception |
| Odometry | `nav_msgs/msg/Odometry` | diff-drive plugin or controller | SLAM, Nav2 |
| Occupancy map | `nav_msgs/msg/OccupancyGrid` | SLAM Toolbox / map_server | AMCL, Nav2 |
| Navigate to pose | `nav2_msgs` action `NavigateToPose` | mission / BT | Nav2 |
| Follow waypoints | `nav2_msgs` action `FollowWaypoints` | mission / BT | Nav2 `waypoint_follower` |

Until the robot is running, **SENTRA publishes none of these.**

### 3.3 Inspection report (data design)

First implementation: append-only JSON Lines or a YAML list on disk under something like `evaluation/runs/<timestamp>/report.json`.

Example record shape (not a ROS message yet):

```json
{
  "checkpoint_id": "cp_01",
  "timestamp_utc": "2026-10-31T00:00:00Z",
  "pose_map": {"x": 0.0, "y": 0.0, "yaw": 0.0},
  "status": "uncertain",
  "category": null,
  "confidence": null,
  "notes": "vision not implemented"
}
```

Why files first:

- Milestone 5 needs durable logs.
- RViz and Nav2 do not need this structure.
- Changing a JSON schema is cheaper than regenerating a ROS interface package.

## 4. Simulation integration (`ros_gz`)

Gazebo Harmonic does not use the old `gazebo_ros` Classic stack. Jazzy talks to Harmonic through **`ros_gz`**:

- `ros_gz_sim` launches or connects to `gz sim`.
- `ros_gz_bridge` converts Gazebo transport topics to ROS 2 topics.
- `ros_gz_image` handles image streaming efficiently.

Launch files and bridge YAML will live in `sentra_gazebo` when that package exists. Exact bridge keys must match the sensor names in the SDF/URDF, so they cannot be finalized before the robot model exists.

## 5. Navigation stack (Milestone 2)

Planned two-phase operation:

1. **Mapping mode:** teleop or cautious autonomy + SLAM Toolbox → save map with `nav2_map_server` tools (`map_saver_cli` when we reach that step).
2. **Localization mode:** load map, run AMCL, run Nav2 planner/controller/behaviors/bt_navigator.

Global vs local costmap (concept):

- **Global costmap:** long-range occupancy used by the planner to find a path from start to goal on the map.
- **Local costmap:** short-range, updated from live LiDAR, used by the controller to avoid new obstacles.

This will be configured with Nav2 parameter YAML. We will start from an official Nav2 / Jazzy example and change only what SENTRA’s robot and world require.

## 6. Perception (Milestone 3)

Pipeline concept:

```text
camera Image → OpenCV preprocess → YOLO inference → detections
                                              ↓
                                    mission / report
```

Rules:

- No pretrained “factory anomaly” model will be assumed.
- Dataset collection, annotation, train/val split, and metrics come **before** claiming inspection works.
- Low-confidence outputs are recorded as `uncertain`, not as findings.

## 7. Behavior tree (Milestone 4)

Conceptual tree (not XML yet):

```text
Fallback (mission)
 ├─ Sequence (inspection patrol)
 │   ├─ For each checkpoint:
 │   │    Sequence
 │   │     ├─ NavigateToCheckpoint
 │   │     ├─ ConfirmNavSuccess
 │   │     ├─ CaptureImage
 │   │     ├─ RunInspection
 │   │     └─ RecordFinding
 │   └─ ReturnToBase
 └─ Sequence (unrecoverable)
      ├─ StopRobot
      ├─ RecordAbort
      └─ WaitForHuman
```

Recovery nodes will have retry counts and timeouts. Nav2 already ships recovery behaviors (spin, backup, wait). SENTRA should **use those first** instead of writing a custom recovery planner.

Nav2 on Jazzy includes `nav2_bt_navigator` and `nav2_behavior_tree`. SENTRA’s mission tree may wrap Nav2 (application layer) rather than replacing Nav2’s internal tree. That choice will be made in Milestone 4 after M2 works.

## 8. Language choice

| Area | Language | Why |
|---|---|---|
| URDF/Xacro, launch, params | XML / Python launch / YAML | Standard ROS 2 |
| Robot description helpers | Python or none | Keep M1 small |
| High-rate control (if custom) | C++ | Only if Python is insufficient |
| Perception node | Python first | OpenCV + later PyTorch are Python-first |
| Behavior tree nodes | C++ (BehaviorTree.CPP) or Nav2 BT plugins | Native BT.CPP is C++; Python BT is a later discussion |
| Reports / evaluation | Python | Fast to iterate |

We will not write C++ and Python duplicates of the same node.

## 9. What we will not do yet

- Create packages without approval.
- Install PyTorch, CUDA, or YOLO tools.
- Design a custom ROS message.
- Copy TurtleBot launch files and relabel them SENTRA without understanding frames and sensors.
- Mark Milestone 1 complete after writing URDF only.

## 10. Appearance and world (agreed direction)

- **Robot look:** industrial inspection platform (low chassis, sensor mast, LiDAR, camera, visible industrial coloring). Not a featureless box. Geometry stays simple enough to write in Xacro; we will not start with a heavy CAD import.
- **World:** custom factory interior built for SENTRA (corridors, obstacles, inspection stations, base pose). Start coarse, then add detail.
- **Drive type:** differential drive unless a later requirement forces a change.

## 11. First implementation slice (after approval)

When implementation is approved, the first package should be **`sentra_description` only**:

- Inputs: none (static model files).
- Outputs: `robot_description` (URDF string) for `robot_state_publisher`.
- Dependencies: `xacro`, `robot_state_publisher`, `rviz2` (for a display launch).
- Does not depend on Gazebo, Nav2, or vision.

Gazebo spawn comes immediately after the model displays correctly in RViz2.
