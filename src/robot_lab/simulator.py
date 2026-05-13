"""Matplotlib visualizers for the two-link robot arm."""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox


MIN_JOINT_COUNT = 1
MAX_JOINT_COUNT = 10


def _format_point(point):
    """Format an x, y point so it is easy to read in the UI."""
    return f"({point[0]:.3f}, {point[1]:.3f})"


def _validate_joint_count(joint_count):
    """Check that the visual joint count is inside the allowed range."""
    if joint_count < MIN_JOINT_COUNT or joint_count > MAX_JOINT_COUNT:
        raise ValueError("Joint count must be between 1 and 10.")


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


class RobotArmSimulator:
    """Interactive matplotlib simulator for a simple two-link robot arm."""

    def __init__(self, robot_arm, target=(1.0, 1.0), joint_count=2):
        _validate_joint_count(joint_count)

        self.robot_arm = robot_arm
        self.target = target
        self.joint_count = joint_count
        self.status_message = "Enter a target and press Move."
        self.joint_buttons = {}

        self.fig, self.ax = plt.subplots(figsize=(9, 6))
        if self.fig.canvas.manager is not None:
            self.fig.canvas.manager.set_window_title("2D Robot Arm Simulator")
        self.fig.subplots_adjust(left=0.08, right=0.70, bottom=0.22)

        self.info_text = self.fig.text(
            0.73,
            0.80,
            "",
            fontsize=10,
            va="top",
            family="monospace",
        )
        self.status_text = self.fig.text(
            0.73,
            0.30,
            self.status_message,
            fontsize=10,
            va="top",
            color="tab:blue",
        )
        self.joint_label = self.fig.text(
            0.73,
            0.50,
            "Joint count",
            fontsize=10,
            va="top",
        )

        self.target_x_box = self._create_text_box([0.16, 0.07, 0.18, 0.06], "Target x", target[0])
        self.target_y_box = self._create_text_box([0.44, 0.07, 0.18, 0.06], "Target y", target[1])

        button_ax = self.fig.add_axes([0.70, 0.07, 0.16, 0.06])
        self.move_button = Button(button_ax, "Move")
        self._create_joint_buttons()

        self.target_x_box.on_submit(self.move_to_input_target)
        self.target_y_box.on_submit(self.move_to_input_target)
        self.move_button.on_clicked(self.move_to_input_target)

        self.move_to_target(target[0], target[1])

    def _create_text_box(self, position, label, value):
        """Create one target input box."""
        text_box_ax = self.fig.add_axes(position)
        return TextBox(text_box_ax, label, initial=str(value))

    def _create_joint_buttons(self):
        """Create buttons for choosing 1 to 10 displayed joints."""
        button_width = 0.038
        button_height = 0.045
        start_x = 0.73
        start_y = 0.43
        x_gap = 0.045
        y_gap = 0.058

        for joint_count in range(MIN_JOINT_COUNT, MAX_JOINT_COUNT + 1):
            index = joint_count - 1
            row = index // 5
            column = index % 5
            button_ax = self.fig.add_axes(
                [
                    start_x + column * x_gap,
                    start_y - row * y_gap,
                    button_width,
                    button_height,
                ]
            )
            button = Button(button_ax, str(joint_count))
            button.on_clicked(self._make_joint_button_handler(joint_count))
            self.joint_buttons[joint_count] = button

        self._update_joint_button_colors()

    def _make_joint_button_handler(self, joint_count):
        """Create a click handler for one joint-count button."""
        def handle_click(_event):
            self.set_joint_count(joint_count)

        return handle_click

    def set_joint_count(self, joint_count):
        """Change how many arm joints are displayed in the simulator."""
        _validate_joint_count(joint_count)

        self.joint_count = joint_count
        self.status_message = f"Joint count set to {joint_count}."
        self._update_joint_button_colors()
        self._draw()

    def _update_joint_button_colors(self):
        """Highlight the currently selected joint-count button."""
        for joint_count, button in self.joint_buttons.items():
            if joint_count == self.joint_count:
                button.ax.set_facecolor("lightblue")
            else:
                button.ax.set_facecolor("0.85")

    def move_to_input_target(self, _event=None):
        """Read target x, y from the input boxes and move the arm."""
        try:
            target_x = float(self.target_x_box.text)
            target_y = float(self.target_y_box.text)
        except ValueError:
            self.status_message = "Target x and y must be numbers."
            self._draw()
            return

        self.move_to_target(target_x, target_y)

    def move_to_target(self, target_x, target_y):
        """Move the robot arm to the target point if it is reachable."""
        self.target = (target_x, target_y)

        try:
            self.robot_arm.move_to(target_x, target_y)
        except ValueError as error:
            self.status_message = str(error)
        else:
            self.status_message = f"Moved to target {_format_point(self.target)}."

        self._draw()

    def _get_display_points(self):
        """Return points used to draw the selected number of visual joints."""
        positions = self.robot_arm.get_joint_positions()
        base = positions["base"]
        elbow = positions["elbow"]
        end_effector = positions["end_effector"]

        if self.joint_count == 1:
            return [base, end_effector]

        if self.joint_count == 2:
            return [base, elbow, end_effector]

        points = []
        total_length = self.robot_arm.link1 + self.robot_arm.link2

        for point_index in range(self.joint_count + 1):
            distance = total_length * point_index / self.joint_count

            if distance <= self.robot_arm.link1:
                ratio = distance / self.robot_arm.link1
                x = base[0] + (elbow[0] - base[0]) * ratio
                y = base[1] + (elbow[1] - base[1]) * ratio
            else:
                ratio = (distance - self.robot_arm.link1) / self.robot_arm.link2
                x = elbow[0] + (end_effector[0] - elbow[0]) * ratio
                y = elbow[1] + (end_effector[1] - elbow[1]) * ratio

            points.append((x, y))

        return points

    def _draw(self):
        """Redraw the robot arm, target point, and position information."""
        positions = self.robot_arm.get_joint_positions()
        base = positions["base"]
        end_effector = positions["end_effector"]
        display_points = self._get_display_points()

        x_points = [point[0] for point in display_points]
        y_points = [point[1] for point in display_points]
        middle_points = display_points[1:-1]

        self.ax.clear()
        self.ax.plot(x_points, y_points, "-o", linewidth=4, markersize=9, label="Robot arm")
        self.ax.scatter(base[0], base[1], s=120, color="black", label="Base")
        if middle_points:
            self.ax.scatter(
                [point[0] for point in middle_points],
                [point[1] for point in middle_points],
                s=90,
                color="tab:orange",
                label="Joint",
            )
        self.ax.scatter(
            end_effector[0],
            end_effector[1],
            s=120,
            color="tab:green",
            label="End-effector",
        )
        self.ax.scatter(
            self.target[0],
            self.target[1],
            s=130,
            color="tab:red",
            marker="x",
            label="Target",
        )

        max_reach = self.robot_arm.link1 + self.robot_arm.link2
        padding = 0.25
        axis_limit = max_reach + padding

        self.ax.set_xlim(-axis_limit, axis_limit)
        self.ax.set_ylim(-axis_limit, axis_limit)
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlabel("x position")
        self.ax.set_ylabel("y position")
        self.ax.set_title("2D Robot Arm Simulator")
        self.ax.grid(True)
        self.ax.legend(loc="upper right")

        self.info_text.set_text(
            "Position\n"
            f"Base: {_format_point(base)}\n"
            f"End : {_format_point(end_effector)}\n\n"
            "Target\n"
            f"x   : {self.target[0]:.3f}\n"
            f"y   : {self.target[1]:.3f}\n\n"
            f"Joints: {self.joint_count}"
        )
        self.status_text.set_text(self.status_message)

        self.fig.canvas.draw_idle()

    def show(self):
        """Show the simulator window."""
        plt.show()


def show_interactive_arm(robot_arm, target=(1.0, 1.0)):
    """Open an interactive simulator window."""
    simulator = RobotArmSimulator(robot_arm, target)
    simulator.show()
    return simulator
