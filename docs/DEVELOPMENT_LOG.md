# SENTRA development log

Format for each entry: date, work completed, problems, solutions, engineering decisions, lessons.

Entries must not claim implementation that did not happen.

---

## 2026-10-31 — Project start: inspect workspace and write baseline docs

### Work completed

- Inspected `/home/tharun/sentra_ws`. Found empty `src/`, empty `evaluation/`, `media/`, `scripts/`, and empty Markdown placeholders.
- Confirmed Git repository exists on `main` with no commits and no remote.
- Verified host: Ubuntu 24.04.5 on WSL2, ROS 2 Jazzy sourced from `~/.bashrc`.
- Verified Gazebo Harmonic (`gz sim` 8.15.0), `ros_gz`, RViz2, Nav2, SLAM Toolbox, BehaviorTree.CPP 4.10, xacro, teleop, `ros2_control`, `gz_ros2_control`, OpenCV 4.6 via `python3-opencv`.
- Verified gaps: no PyTorch, no Ultralytics, no SENTRA packages, no colcon build artifacts, GPU not usable in this WSL instance (`nvidia-smi` blocked, no `/dev/dxg`), OpenGL is Mesa llvmpipe (unaccelerated).
- Wrote initial `README.md`, `docs/PROJECT_OVERVIEW.md`, `docs/PROJECT_STATE.md`, `docs/DEVELOPMENT_LOG.md`, and `design/SYSTEM_ARCHITECTURE.md`.
- Did **not** install packages, create ROS 2 packages, or write robot/source code.

### Problems encountered

- Documentation files existed as empty stubs, so the repository looked initialized but had no content.
- GPU access is blocked in WSL, which affects Gazebo performance and later YOLO training.

### Solutions

- Replaced empty docs with evidence-based project records.
- Recorded GPU/GUI limits honestly instead of assuming a full robotics desktop.

### Engineering decisions

1. **Documentation before packages.** Architecture and environment facts come first so package names are not invented under time pressure.
2. **Few packages, created only when needed.** Proposed set (pending approval): `sentra_description`, `sentra_gazebo`, `sentra_navigation`, `sentra_perception`, `sentra_mission`, `sentra_bringup`. No custom interface package until a real message/service/action is required.
3. **Standard ROS 2 message types first.** Sensor, nav, and geometry messages from common interfaces; inspection reports as JSON/YAML on disk in the first version.
4. **Object detection, not claimed anomaly detection.** Inspection starts with trained classes after a dataset exists.
5. **Recommended kinematics: differential drive.** Indoor factory patrol does not need omnidirectional or Ackermann bases for the first robot.
6. **Do not install PyTorch/YOLO now.** That belongs to Milestone 3 and needs a resource discussion (CPU vs GPU).

### Lessons learned

- A folder named `src/` does not mean a ROS 2 workspace has packages or a successful overlay. Check for `package.xml` and `install/`.
- Jazzy on Ubuntu 24.04 already provides most of the robotics stack SENTRA needs. The missing pieces are project code, a dataset, and (later) a local detector toolchain.
- WSL2 can have a working `DISPLAY` and still have no GPU acceleration. Simulation plans must assume CPU rendering until proven otherwise.

### Follow-up

- Wait for student confirmation of architecture.
- Recommended next practical step: GUI smoke test of Gazebo Harmonic and RViz2.

---

## 2026-10-31 — Visual style, custom world, GitHub naming

### Work completed

- Recorded two student decisions: industrial robot appearance; custom factory world built in-project.
- Documented a recommended GitHub repository name and description. The GitHub remote was **not** created in this step.

### Engineering decisions

1. **Appearance vs kinematics.** “Industrial look” means the visible model (chassis, mast, sensors, factory-style colors). It does **not** change the first drive type: differential drive is still the right kinematics for indoor patrol.
2. **Custom world.** Checkpoints, aisles, and inspection props will be designed for SENTRA rather than depending on an unmodified download. Complexity stays low at the start (walls, floor, a few machines, marked inspection poses).
3. **GitHub.** A new public repository named `sentra` is recommended for the portfolio. Create it after a `.gitignore` and a first local commit so `build/`, `install/`, and large sim artifacts are never pushed.

### Lessons learned

- Visual fidelity and mobility type are separate design choices. A robot can look like an industrial inspector and still be a two-wheel differential base.

---

## 2026-10-31 — Git phase workflow and first documentation commit

### Work completed

- Added `.gitignore` for ROS 2 overlay directories, bags, and model weights.
- Recorded the rule: commit and push to GitHub at the end of each completed project phase.
- Created the first local Git commit of documentation.
- GitHub repository already exists and is empty: https://github.com/Tharun0723/Sentra
- Push of `main` is the close of this documentation phase.

### Engineering decisions

1. **Commit by phase, not by file-save.** A phase is a tested slice (for example: docs baseline, robot in RViz, robot in Gazebo). Incomplete experiments stay local until they work or are explicitly abandoned.
2. **Never commit** `build/`, `install/`, `log/`, rosbag files, or `.pt` weights. Maps as YAML+PGM can be committed when they are project assets.
3. **GitHub remote name** remains `sentra` when the repository is created.
