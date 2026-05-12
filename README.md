# AI Robot Arm Control Lab

A beginner-readable Python project for learning the basics of robotic arm motion.

The current phase is a **Python 2D robotic arm simulator**. It models a simple two-link planar robot arm, calculates forward kinematics, solves inverse kinematics, and visualizes the arm with matplotlib.

## Current Phase

Phase 1: Python robotic arm simulator

This phase focuses only on the simulator foundation. It does not include AI, OpenCV, reinforcement learning, LeRobot, or hardware control yet.

## Future Roadmap

- Phase 2: PID control
- Phase 3: OpenCV object detection
- Phase 4: simple AI policy model
- Phase 5: LeRobot/SO-ARM101 extension

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Run the Simulator

From the project root, run:

```bash
python scripts/run_simulator.py
```

The script creates a two-link robot arm, moves it to a target point, and displays the result using matplotlib.

## Run Tests

From the project root, run:

```bash
pytest
```

The tests check the forward kinematics, inverse kinematics, and basic `RobotArm2D` behavior.
