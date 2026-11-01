# SENTRA
### Autonomous Industrial Inspection Robot

**Perceive. Navigate. Inspect.**

SENTRA is a simulation-based autonomous mobile robotics project focused on intelligent industrial inspection. The goal is to develop a customized mobile robot capable of autonomously patrolling a large, purpose-built industrial factory environment, navigating inspection checkpoints, identifying visual anomalies using AI-powered computer vision, generating inspection reports, and recovering from operational failures.

Built using **ROS 2 Jazzy, Gazebo Harmonic, Nav2, SLAM Toolbox, OpenCV, YOLO and BehaviorTree.CPP**, SENTRA aims to demonstrate an integrated autonomous robotics system through simulation.

> This is an actively developed engineering project. Features described below are development objectives unless explicitly marked as implemented.

---

## Project Vision

Industrial facilities require regular monitoring to identify unsafe conditions, misplaced objects and potential operational hazards.

SENTRA explores how autonomous mobile robots can assist with these inspections through a combination of:

- Autonomous mobile robotics.
- Environmental mapping and localization.
- Intelligent navigation and path planning.
- AI-powered visual perception.
- Autonomous mission planning.
- Failure detection and recovery.

The long-term objective is to build a complete, modular and testable autonomous inspection platform.

## Key Objectives

- Design a customized industrial mobile robot using URDF and Xacro.
- Develop a detailed, large-scale factory environment in Gazebo Harmonic.
- Integrate LiDAR, IMU, RGB camera and odometry.
- Implement autonomous mapping using SLAM Toolbox.
- Implement localization and autonomous navigation using Nav2.
- Develop an AI-powered visual inspection pipeline using OpenCV and YOLO.
- Detect selected industrial anomalies and generate inspection reports.
- Coordinate inspection missions using BehaviorTree.CPP.
- Implement intelligent recovery strategies for navigation and perception failures.
- Evaluate system reliability through at least 30 simulation runs.

## Planned System Capabilities

| Subsystem | Planned functionality |
|---|---|
| Robot design | Custom industrial mobile robot |
| Simulation | Large custom industrial factory |
| Perception | LiDAR, IMU, camera and odometry |
| Mapping | 2D SLAM using SLAM Toolbox |
| Localization | AMCL and TF2 |
| Navigation | Nav2 and waypoint navigation |
| Computer vision | OpenCV and YOLO |
| AI resources | Hugging Face models and datasets where suitable |
| Mission control | BehaviorTree.CPP |
| Recovery | Navigation and perception recovery |
| Reporting | Structured inspection reports |
| Evaluation | Mission success, detection performance and failure analysis |

## Inspection Scenarios

The initial inspection scenarios will explore:

1. Liquid spills and floor hazards.
2. Missing or incorrectly placed safety equipment.
3. Misplaced industrial objects.

The detection categories, datasets and models will be selected and evaluated during development.

## Technology Stack

| Category | Technology |
|---|---|
| Operating system | Ubuntu 24.04 |
| Development environment | Windows 11 + WSL2 |
| Robotics middleware | ROS 2 Jazzy |
| Simulation | Gazebo Harmonic |
| Simulation integration | ros_gz |
| Robot description | URDF / Xacro |
| Visualization | RViz2 |
| Mapping | SLAM Toolbox |
| Localization | AMCL |
| Navigation | Nav2 |
| Behavior trees | BehaviorTree.CPP |
| Computer vision | OpenCV |
| Deep learning | PyTorch |
| Object detection | YOLO |
| AI model resources | Hugging Face |
| Programming | C++ and Python |
| Version control | Git and GitHub |
| IDE | Cursor |

The project prioritizes free and open-source software and local execution wherever practical.

## System Architecture

The intended system is organized into modular subsystems:

1. Robot Description and Simulation
2. Sensor Integration and Processing
3. Mapping and Localization
4. Autonomous Navigation
5. AI-based Visual Inspection
6. Inspection Mission Management
7. Behavior Tree and Recovery
8. Inspection Reporting and Evaluation

Each subsystem will be developed and tested incrementally before integration.

## Development Roadmap

### Milestone 1 — Robot Foundation
- Custom robot design.
- URDF/Xacro modelling.
- RViz visualization.
- Gazebo integration.
- Sensor integration.
- Keyboard teleoperation.

### Milestone 2 — Mapping and Navigation
- Factory environment development.
- SLAM mapping.
- Map saving and loading.
- Localization.
- Nav2 configuration.
- Autonomous checkpoint navigation.

### Milestone 3 — AI Computer Vision
- Camera integration.
- OpenCV image processing.
- Dataset preparation.
- YOLO model selection or training.
- Anomaly detection.
- ROS 2 detection pipeline.

### Milestone 4 — Autonomous Inspection
- BehaviorTree.CPP integration.
- Inspection checkpoint management.
- Navigation and perception integration.
- Inspection reporting.
- Failure detection and recovery.

### Milestone 5 — Testing and Evaluation
- At least 30 inspection runs.
- Navigation performance evaluation.
- Detection performance evaluation.
- Failure analysis.
- Reliability improvements.
- Documentation and demonstration video.

## Current Development Status

**Current milestone: Milestone 1 — Robot Foundation**

| Component | Current status |
|---|---|
| ROS 2 Jazzy environment | Installed |
| Gazebo Harmonic | Installed |
| RViz2 | Installed |
| SENTRA ROS 2 workspace | Created |
| `sentra_description` package | Created and builds |
| Robot Xacro description | Created; RViz verification pending |
| Gazebo robot spawning | Pending |
| Custom factory world | Pending |
| SLAM and Nav2 | Pending integration |
| AI vision pipeline | Pending |
| Behavior tree mission | Pending |

Progress will be updated as each component is implemented and tested.

## Repository Structure

```text
sentra_ws/
├── src/
│   └── sentra_description/
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── PROJECT_STATE.md
│   └── DEVELOPMENT_LOG.md
├── design/
│   └── SYSTEM_ARCHITECTURE.md
├── evaluation/
├── media/
├── scripts/
└── README.md
```

Additional ROS 2 packages will be introduced as the architecture develops.

## Development Environment

The project is developed using:

- Windows 11.
- WSL2.
- Ubuntu 24.04.
- ROS 2 Jazzy.
- Gazebo Harmonic.

Workspace:

```bash
~/sentra_ws
```

Detailed installation, build and execution instructions will be maintained as the project progresses.

## Evaluation Goals

The final system will be evaluated using:

- Mission completion rate.
- Navigation success rate.
- Localization reliability.
- Detection precision, recall and related metrics.
- Inspection completion time.
- Failure recovery success rate.

Results will be documented using reproducible simulation experiments.

## Project Documentation

- `docs/PROJECT_OVERVIEW.md` — Project requirements and objectives.
- `docs/PROJECT_STATE.md` — Verified implementation status.
- `docs/DEVELOPMENT_LOG.md` — Development history and engineering decisions.
- `design/SYSTEM_ARCHITECTURE.md` — System architecture and interfaces.

## Learning and Engineering Philosophy

SENTRA is being developed as a hands-on robotics engineering project.

The emphasis is on understanding robotics fundamentals, designing modular systems, implementing algorithms, debugging real integration problems and evaluating performance rather than simply assembling existing code.

## License

To be decided.

---

**SENTRA — Perceive. Navigate. Inspect.**

Do not commit `build/`, `install/`, `log/`, bag files, or neural-network weights. Those are listed in `.gitignore`.

## License

Not chosen yet.
