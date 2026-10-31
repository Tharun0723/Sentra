# SENTRA project state

**Date of this snapshot:** 31 October 2026  
**Current milestone:** Milestone 1 — Robot Foundation (**not started**)  
**Implementation status:** Documentation only. No ROS 2 packages, no robot model, no simulation world.

This file records **verified** facts. If something was not checked, it is marked unknown.

## 1. Workspace

Path: `/home/tharun/sentra_ws`

```
sentra_ws/
  README.md
  design/SYSTEM_ARCHITECTURE.md
  docs/PROJECT_OVERVIEW.md
  docs/PROJECT_STATE.md
  docs/DEVELOPMENT_LOG.md
  evaluation/          (empty)
  media/               (empty)
  scripts/             (empty)
  src/                 (empty — no package.xml files)
```

There is **no** `build/`, `install/`, or `log/` directory. `colcon` has never built this workspace.

Git: local repository on branch `main`. `.gitignore` excludes colcon artifacts, bags, and model weights.

GitHub (empty until first push): https://github.com/Tharun0723/Sentra

**Phase rule:** after each completed, tested phase — update docs, commit, push.

## 2. Host environment (verified)

| Item | Evidence |
|---|---|
| Kernel | `Linux ... microsoft-standard-WSL2` |
| Distro | Ubuntu 24.04.5 LTS (`noble`) |
| CPU | 12 processors (`nproc`) |
| RAM | ~15 GiB total |
| Disk | ~1007G workspace filesystem, ~7.8G used |
| Display | `DISPLAY=:0`, `WAYLAND_DISPLAY=wayland-0` |
| OpenGL | Mesa **llvmpipe** (software). `Accelerated: no` |
| NVIDIA | `nvidia-smi` reported GPU access blocked; `/dev/dxg` absent |

Implication: Gazebo and RViz can likely open, but rendering is CPU-based. This will be slower than GPU-accelerated simulation. GUI launch has **not** been smoke-tested yet.

`~/.bashrc` sources `/opt/ros/jazzy/setup.bash`.

## 3. ROS 2 and simulation (verified)

| Component | Status | Evidence |
|---|---|---|
| ROS 2 Jazzy | Installed and sourced | `ROS_DISTRO=jazzy`, `/opt/ros/jazzy/setup.bash` exists |
| `ros2` CLI | On PATH | `/opt/ros/jazzy/bin/ros2` |
| Desktop metapackage | Installed | `ros-jazzy-desktop` |
| desktop-full | Not installed | `dpkg` missing |
| Gazebo Harmonic | Installed | package `gz-harmonic`; `gz sim --versions` → **8.15.0** |
| `ros_gz` | Installed | `ros-jazzy-ros-gz`, `ros_gz_sim`, `ros_gz_bridge`, `ros_gz_image` |
| RViz2 | Installed | `ros-jazzy-rviz2`; `ros2 pkg list` includes `rviz2` |
| Nav2 | Installed | `ros-jazzy-navigation2`, `nav2_bringup`, `nav2_amcl`, waypoint follower, simple commander |
| SLAM Toolbox | Installed | `ros-jazzy-slam-toolbox` 2.8.5 |
| BehaviorTree.CPP | Installed | `ros-jazzy-behaviortree-cpp` 4.10.0 |
| Xacro / URDF / TF | Installed | `xacro`, `urdf`, `tf2_ros`, `robot_state_publisher` |
| Teleop | Installed | `teleop_twist_keyboard`, `teleop_twist_joy` |
| ros2_control | Installed | `ros2_control`, `diff_drive_controller`, `gz_ros2_control` |
| Vision ROS pkgs | Partial | `cv_bridge`, `image_transport` installed; `ros-jazzy-vision-opencv` metapackage **missing** (cv_bridge itself is present) |
| `twist_mux` | Not installed | optional, not required yet |
| `laser_filters` | Not installed | optional, not required yet |
| colcon | Installed | `/usr/bin/colcon` plus common extensions |
| Python | 3.12.3 | system Python |
| OpenCV | Installed | `python3-opencv` → `cv2` 4.6.0 |
| NumPy / PyYAML | Installed | numpy 1.26.4; PyYAML importable |
| PyTorch | **Not** importable | `import torch` failed |
| Ultralytics YOLO | **Not** importable | `import ultralytics` failed |

### 3.1 ROS 2 packages that exist as Debian installs (selected)

Present on this machine and listed by `ros2 pkg list`: `nav2_*` (including `nav2_amcl`, `nav2_bringup`, `nav2_waypoint_follower`, `nav2_simple_commander`, `nav2_behavior_tree`), `slam_toolbox`, `ros_gz*`, `rviz2`, `teleop_twist_keyboard`, `xacro`, `robot_state_publisher`, `cv_bridge`, `behaviortree_cpp`, `gz_ros2_control`.

Also present: `nav2_minimal_tb3_sim`, `nav2_minimal_tb4_description`, `nav2_minimal_tb4_sim`. These are **upstream examples**, not SENTRA packages.

## 4. SENTRA software (verified)

| Item | Status |
|---|---|
| Custom packages | None |
| Topics / services / actions owned by SENTRA | None |
| Launch files | None |
| Maps | None |
| Datasets / models | None |
| Inspection reports | None |

A ROS 2 workspace overlay is **not** initialized in the colcon sense: `src/` exists but contains no packages, and the workspace has never been built.

## 5. Known errors

None from SENTRA software, because none exists.

Environment risks (not yet reproduced as failures):

- Software rendering may make Gazebo Harmonic heavy on WSL2.
- GPU-backed YOLO training is not available on this WSL instance until GPU access is fixed **or** CPU training is explicitly accepted (slow).

## 6. Completed tasks

- Inspected workspace tree.
- Read existing documentation files (they were empty placeholders).
- Verified ROS 2 Jazzy, Gazebo Harmonic, Nav2, SLAM Toolbox, `ros_gz`, RViz2, teleop, and related packages with `dpkg` / `ros2 pkg list` / version commands.
- Wrote initial Markdown documentation (`README.md`, `docs/*`, `design/SYSTEM_ARCHITECTURE.md`).

## 7. Pending tasks

- Student review of remaining architecture details (package list, GUI smoke test).
- GUI smoke test: empty Gazebo Harmonic world + RViz2 (no custom packages).
- Create GitHub remote when the student is ready (recommended name: `sentra`).
- Only after architecture approval: first ROS 2 package for robot description.

## 8. Next recommended task

**Do not create packages yet.** First confirm that the GUI simulation stack actually opens on this WSL2 machine:

1. Launch an empty Gazebo Harmonic world.
2. Launch RViz2.
3. Confirm both windows appear and remain stable for a short time.

Exact commands will be given when that task is started. No extra apt packages are required for that test.

## 9. Design decisions already made

| Topic | Decision | Date |
|---|---|---|
| Drive type | Differential drive (two driven wheels + support caster/wheels) | 2026-10-31 (recommended; not contradicted) |
| Visual design | Industrial inspection look, not a plain box chassis | 2026-10-31 |
| World | Custom factory world, built in the project (not an unmodified third-party world) | 2026-10-31 |

## 10. Missing information (still open)

- Checkpoint count (recommendation remains 4–6 plus base).
- Exact inspection object classes for Gazebo (spills, PPE, misplaced parts are still only ideas).
- Public vs private GitHub, license.
- GPU passthrough vs CPU-only for later YOLO work.
- Gazebo diff-drive plugin first vs `gz_ros2_control` from day one.
