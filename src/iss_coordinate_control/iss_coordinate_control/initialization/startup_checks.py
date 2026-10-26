
"""Startup readiness checks for the ISS XYZ gantry."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StartupStatus:
    """Results reported by startup and ROS interface checks."""

    ros_initialized: bool = False
    robot_description_loaded: bool = False
    controller_ready: bool = False
    joint_feedback_available: bool = False


@dataclass(frozen=True)
class StartupResult:
    """Combined startup decision."""

    successful: bool
    failures: tuple[str, ...]


def check_startup(status: StartupStatus) -> StartupResult:
    """Evaluate whether required startup conditions passed."""
    failures = []

    checks = {
        "ROS 2 initialized": status.ros_initialized,
        "Robot description loaded":
            status.robot_description_loaded,
        "Motion controller ready":
            status.controller_ready,
        "Joint feedback available":
            status.joint_feedback_available,
    }

    for name, passed in checks.items():
        if not passed:
            failures.append(name)

    return StartupResult(
        successful=(len(failures) == 0),
        failures=tuple(failures),
    )
