"""Run a small example of the 2D robot arm simulator."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from robot_lab.arm import RobotArm2D
from robot_lab.simulator import show_arm


def main():
    arm = RobotArm2D(link1=1.0, link2=1.0)

    target_x = 1.0
    target_y = 1.0

    arm.move_to(target_x, target_y)
    end_x, end_y = arm.get_end_effector()

    print(f"Moved end-effector to approximately ({end_x:.3f}, {end_y:.3f})")
    show_arm(arm, target=(target_x, target_y))


if __name__ == "__main__":
    main()
