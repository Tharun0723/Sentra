# SENTRA project overview

## 1. What SENTRA is

SENTRA (Autonomous Industrial Inspection Robot) is a **student robotics engineering project** in simulation.

The intended mission is:

1. Operate inside a simulated factory.
2. Localize on a map of that factory.
3. Navigate to a sequence of inspection checkpoints.
4. Capture a camera image at each checkpoint.
5. Run a visual inspection model on that image.
6. Record a structured finding.
7. Continue, return to a base pose, and stop.
8. Detect a defined set of failures and recover within stated limits.

The project is **not** a physical robot, not a commercial product, and not an already-working system. It is a planned software architecture that will be implemented in five milestones.

## 2. Why this project exists

The educational goal is to become an AI robotics engineer who can:

- Use ROS 2 as the communication and lifecycle layer, not only as a collection of launch files.
- Model a mobile robot, connect sensors, and understand TF2 frames.
- Map an environment, localize, and navigate with Nav2.
- Collect a dataset, train a detector, and be honest about what the detector can and cannot do.
- Coordinate a mission with a behavior tree instead of a single long script.
- Document, test, and present the work as a professional portfolio project.

## 3. Constraints

| Constraint | Implication |
|---|---|
| Student budget | Free and open-source tools only |
| Local computation | No paid cloud APIs for perception or LLMs |
| Simulation-first | Gazebo Harmonic + `ros_gz` is the robot “hardware” |
| ROS 2 Jazzy / Gazebo Harmonic | Do not copy Humble/Garden/Fortress instructions blindly |
| Learning project | Small steps, explanations, and tests before new packages |
| Honesty | Planned work is documented as planned, not as implemented |

## 4. Functional requirements

These are **target** requirements. None of them are implemented in software yet.

### 4.1 Environment

A simulated industrial interior with floors, walls, corridors, obstacles, inspection checkpoints, and a designated base pose.

### 4.2 Robot

A ground mobile robot that can:

- Drive with a velocity command (`geometry_msgs/msg/Twist` or the equivalent stamped command used by the chosen controller).
- Sense range with LiDAR.
- Sense orientation/motion with an IMU.
- Estimate motion with wheel odometry.
- Capture RGB images with a camera.

### 4.3 Mapping and localization

- Build a 2D occupancy map with SLAM Toolbox.
- Save and reload that map.
- Localize on the saved map (planned: AMCL from Nav2).

### 4.4 Navigation

- Send a pose goal and have Nav2 plan and follow a path.
- Visit a waypoint list of checkpoints.
- Report success, failure, or timeout.
- Return to base after the mission or after an unrecoverable failure.

### 4.5 Visual inspection

- Receive camera images on a ROS 2 image topic.
- Process images with OpenCV.
- Detect a **defined, trained** set of object or scene classes with YOLO after a dataset exists.
- Publish structured results.
- Distinguish **object detection** (the model found a trained class) from **anomaly detection** (the scene is unusual compared with a model of normality). SENTRA will start as object/scene classification of known inspection categories. It will not be described as reliable anomaly detection unless that is separately designed and evaluated.

### 4.6 Mission control

A behavior tree coordinates: start → navigate → confirm → inspect → record → next checkpoint → return to base.

### 4.7 Failure handling

Supported failure classes (to be implemented later, with limits):

| Failure | Intended response (concept) |
|---|---|
| Blocked / stuck | Bounded recovery behaviors, then abort and report |
| Navigation goal failed | One or two replans, then skip or abort according to policy |
| Lost localization | Stop, attempt recovery, otherwise require human restart |
| Missing camera data | Skip visual inspection, mark checkpoint as `vision_unavailable` |
| Uncertain detection | Record low confidence; do not invent a finding |
| Inspection timeout | Abort that checkpoint, continue or return based on policy |

Retries will be **bounded**. Infinite retry is not an acceptable design.

### 4.8 Reporting

Each checkpoint produces a record with at least:

- Checkpoint ID
- Timestamp
- Robot position (map frame)
- Detection result
- Category
- Confidence
- Inspection status (`ok`, `finding`, `uncertain`, `vision_unavailable`, `nav_failed`, `timeout`)

Planned storage for the first version: a JSON or YAML file on disk. A custom ROS message will only be added if nodes actually need to share that structure at runtime.

## 5. Non-functional requirements

- Target platform: Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic.
- Reproducible install notes as packages appear.
- Modular packages with a stated reason for each new package.
- Tests and logs before a milestone is marked complete.
- At least 30 inspection runs in Milestone 5, with success rates and failure notes.

## 6. Milestones

| ID | Name | Success looks like |
|---|---|---|
| M1 | Robot foundation | Custom robot in RViz2 and Gazebo; sensors publishing; keyboard teleop |
| M2 | Mapping and navigation | Saved factory map; AMCL localization; Nav2 goals and waypoint patrol |
| M3 | Computer vision | Dataset, trained/adapted detector, ROS 2 results, known class list |
| M4 | Autonomous inspection | Behavior tree runs the full mission with reporting and recovery |
| M5 | Testing and documentation | ≥30 runs, metrics, limitations, GitHub docs, demonstration video |

Milestone 1 is the only milestone that should start after architecture approval. Later milestones must not be coded in advance.

## 7. Learning sequence (how work should happen)

For each technical piece:

1. Explain the concept.
2. Show how it fits SENTRA.
3. Do a small implementation task.
4. Explain the files, nodes, topics, and why the design was chosen.
5. Test with exact commands and expected observations.
6. The student restates the idea in their own words.
7. Commit, update `PROJECT_STATE.md`, log decisions, and push to GitHub at the end of each completed phase.

## 8. Official references (version-specific)

- ROS 2 Jazzy: https://docs.ros.org/en/jazzy/
- Gazebo Harmonic: https://gazebosim.org/docs/harmonic/
- `ros_gz`: https://github.com/gazebosim/ros_gz
- Nav2: https://docs.nav2.org/
- SLAM Toolbox: https://github.com/SteveMacenski/slam_toolbox
- OpenCV: https://docs.opencv.org/
- BehaviorTree.CPP: https://www.behaviortree.dev/

If a tutorial is written for Humble, Iron, Gazebo Classic, Fortress, or Garden, it must be checked against the Jazzy/Harmonic docs before use.
