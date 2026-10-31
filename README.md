# SENTRA

**SENTRA – Autonomous Industrial Inspection Robot**

*Perceive. Navigate. Inspect.*

SENTRA is a **simulation-based** robotics engineering project. The long-term goal is an autonomous mobile robot that patrols a simulated industrial factory, navigates between inspection checkpoints, inspects the scene with a camera, records findings, and recovers from a defined set of navigation and perception failures.

This repository currently contains **project documentation and an empty ROS 2 workspace**. No robot description, simulation world, navigation configuration, or inspection software has been implemented yet.

## Objectives

- Build a complete autonomous inspection stack in **ROS 2 Jazzy** and **Gazebo Harmonic**.
- Demonstrate mapping, localization, Nav2 navigation, computer vision, and behavior-tree mission control.
- Treat the work as a learning project: every subsystem should be understood, tested, and documented before the next one is added.
- Keep the stack **free and local**. Avoid paid APIs, subscriptions, and commercial dependencies.

## Current status

| Item | Status (31 Oct 2026) |
|---|---|
| Project documentation | Initial versions created |
| ROS 2 packages in `src/` | `sentra_description` (RViz display only) |
| Robot URDF / Xacro | Industrial differential-drive model in RViz |
| Gazebo factory world | Not started |
| Mapping, Nav2, vision, mission | Not started |
| Git history | Repository exists, no commits yet |

See [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) for the evidence-based environment report.

## Technology stack

| Role | Choice |
|---|---|
| Host OS | Windows 11 |
| Linux | Ubuntu 24.04 on WSL2 |
| Middleware | ROS 2 Jazzy |
| Simulator | Gazebo Harmonic (`gz sim` 8.x) via `ros_gz` |
| Visualization | RViz2 |
| Mapping | SLAM Toolbox |
| Localization | AMCL (Nav2) |
| Navigation | Nav2 |
| Decision-making | BehaviorTree.CPP |
| Languages | C++ and Python |
| Vision | OpenCV; YOLO via PyTorch (not installed yet) |
| Version control | Git and GitHub |

## Architecture overview

SENTRA is planned as a small set of ROS 2 packages, not one large application.

1. **Robot description and simulation** — model, sensors, factory world, Gazebo bridges.
2. **Mapping and localization** — SLAM Toolbox, saved map, AMCL, TF2.
3. **Autonomous navigation** — Nav2 path planning, control, waypoints.
4. **Computer vision** — camera images, OpenCV, trained detector, inspection results.
5. **Mission management** — behavior tree, reporting, recovery, evaluation.

Package names are **proposals only**. They will not be created until they are approved and needed. Details: [design/SYSTEM_ARCHITECTURE.md](design/SYSTEM_ARCHITECTURE.md).

## Features (target, not implemented)

- Differential-drive mobile robot in Gazebo with LiDAR, IMU, RGB camera, and odometry.
- Manual keyboard teleoperation.
- 2D mapping of a factory environment, then localization on the saved map.
- Waypoint navigation to inspection checkpoints and return to base.
- Visual inspection of a defined set of object/scene categories after a dataset is collected and a model is trained.
- Behavior-tree mission with bounded retries, timeouts, and a human-intervention fallback.
- Inspection reports written to disk for later evaluation.

Do not treat this list as a claim that the robot already does these things.

## Installation and execution

Build the description package, then display it in RViz (this does **not** start Gazebo):

```bash
cd ~/sentra_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select sentra_description
source install/setup.bash
ros2 launch sentra_description display.launch.py
```

On this development machine, ROS 2 Jazzy, Gazebo Harmonic, Nav2, SLAM Toolbox, `ros_gz`, RViz2, and teleop packages are already installed. PyTorch and YOLO tooling are **not**. GUI rendering currently uses software Mesa (`llvmpipe`), not a dedicated GPU.

Full environment details and commands used to verify them are in [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md).

Reproduction notes for a new Ubuntu 24.04 / ROS 2 Jazzy machine will be written when the first packages exist and have been built successfully.

## Demonstration

No demonstration video or recorded mission exists yet.

## Results and limitations

No inspection runs have been performed. There are no navigation, detection, or timing results.

Known environment constraints:

- WSL2 GUI works, but Gazebo/RViz are currently **CPU-rendered**. Simulation will be slower than on a machine with working GPU passthrough.
- YOLO training and inference are not available until a free local PyTorch setup is chosen and installed.
- `twist_mux` and `laser_filters` are not installed. They are optional and will only be added if a clear need appears.

## Documentation map

| File | Purpose |
|---|---|
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Requirements, milestones, learning goals |
| [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) | What exists today, verified against the machine |
| [docs/DEVELOPMENT_LOG.md](docs/DEVELOPMENT_LOG.md) | Decisions, problems, lessons |
| [design/SYSTEM_ARCHITECTURE.md](design/SYSTEM_ARCHITECTURE.md) | Proposed subsystems and ROS 2 interfaces |

## Version control

Work happens on `main` in this workspace. **After each completed phase** (a milestone slice that was tested, not every keystroke):

1. Update `docs/PROJECT_STATE.md` and `docs/DEVELOPMENT_LOG.md`.
2. Commit with a message that says *why* the change exists.
3. Push to GitHub so the remote matches the local project.

Do not commit `build/`, `install/`, `log/`, bag files, or neural-network weights. Those are listed in `.gitignore`.

## License

Not chosen yet.
