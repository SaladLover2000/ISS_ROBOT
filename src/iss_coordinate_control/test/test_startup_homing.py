
"""Tests for gantry startup, safety and homing modules."""

import pytest

from iss_coordinate_control.initialization.startup_checks import (
    StartupStatus,
    check_startup,
)
from iss_coordinate_control.safety.estop_monitor import EStopMonitor
from iss_coordinate_control.homing.homing_sequence import (
    HomingError,
    HomingSequence,
)


def test_startup_all_checks_pass():
    status = StartupStatus(
        ros_initialized=True,
        robot_description_loaded=True,
        controller_ready=True,
        joint_feedback_available=True,
    )
    result = check_startup(status)
    assert result.successful
    assert result.failures == ()


def test_startup_missing_controller():
    status = StartupStatus(
        ros_initialized=True,
        robot_description_loaded=True,
        controller_ready=False,
        joint_feedback_available=True,
    )
    result = check_startup(status)
    assert not result.successful
    assert "Motion controller ready" in result.failures


def test_estop_defaults_to_disabled():
    monitor = EStopMonitor()
    assert not monitor.known
    assert monitor.active
    assert not monitor.motion_permitted


def test_estop_clear_and_active():
    monitor = EStopMonitor()

    monitor.update(False)
    assert monitor.motion_permitted

    monitor.update(True)
    assert monitor.active
    assert not monitor.motion_permitted


def test_complete_homing_sequence():
    home = HomingSequence()

    assert home.current_axis == "X"

    for axis in ("X", "Y", "Z"):
        assert home.current_axis == axis
        assert home.confirm_axis(axis, verified=True)

    assert home.is_homed
    assert home.current_axis is None
    assert home.completed == ["X", "Y", "Z"]


def test_homing_failure():
    home = HomingSequence()

    assert not home.confirm_axis("X", verified=False)
    assert home.failed
    assert not home.is_homed
    assert home.current_axis is None


def test_cannot_skip_homing_axes():
    home = HomingSequence()

    with pytest.raises(HomingError):
        home.confirm_axis("Z", verified=True)


def test_reset_invalidates_homing():
    home = HomingSequence()

    for axis in ("X", "Y", "Z"):
        home.confirm_axis(axis, verified=True)

    assert home.is_homed

    home.reset()

    assert not home.is_homed
    assert home.current_axis == "X"
