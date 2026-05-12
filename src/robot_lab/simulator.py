"""Matplotlib visualizer for the two-link robot arm."""

import matplotlib.pyplot as plt


def plot_arm(robot_arm, target=None):
    """Draw the robot arm and an optional target point."""
    positions = robot_arm.get_joint_positions()
    base = positions["base"]
    elbow = positions["elbow"]
    end_effector = positions["end_effector"]

    x_points = [base[0], elbow[0], end_effector[0]]
    y_points = [base[1], elbow[1], end_effector[1]]

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(x_points, y_points, "-o", linewidth=4, markersize=9, label="Robot arm")
    ax.scatter(base[0], base[1], s=120, color="black", label="Base")
    ax.scatter(elbow[0], elbow[1], s=120, color="tab:orange", label="Elbow")
    ax.scatter(end_effector[0], end_effector[1], s=120, color="tab:green", label="End-effector")

    if target is not None:
        ax.scatter(target[0], target[1], s=130, color="tab:red", marker="x", label="Target")

    max_reach = robot_arm.link1 + robot_arm.link2
    padding = 0.25
    axis_limit = max_reach + padding

    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.set_title("2D Robot Arm Simulator")
    ax.grid(True)
    ax.legend(loc="upper right")

    return fig, ax


def show_arm(robot_arm, target=None):
    """Draw the robot arm and show the matplotlib window."""
    plot_arm(robot_arm, target)
    plt.show()
