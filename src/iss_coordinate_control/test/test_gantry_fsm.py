
"""Unit tests for the ISS XYZ gantry state machine."""

import pytest

from iss_coordinate_control.state_machine.gantry_fsm import (
    GantryFSM,
    InvalidTransition,
)
from iss_coordinate_control.state_machine.states import (
    GantryEvent as E,
    GantryState as S,
)


def initialize_to_ready(fsm):
    """Bring the FSM to READY with simulated events."""
    for event in (
        E.POWER_ON,
        E.INITIALIZATION_OK,
        E.ESTOP_CLEAR,
        E.HOME_REQUIRED,
        E.HOMING_SUCCEEDED,
    ):
        fsm.trigger(event)

    assert fsm.state == S.READY


def prepare_move(fsm):
    """Simulate a valid coordinate request."""
    for event in (
        E.COMMAND_RECEIVED,
        E.COMMAND_VALID,
        E.LIMITS_OK,
        E.PATH_SAFE,
    ):
        fsm.trigger(event)

    assert fsm.state == S.MOVING_TO_TARGET


def test_initialization_and_homing():
    """Startup and successful homing reach READY."""
    fsm = GantryFSM()
    initialize_to_ready(fsm)


def test_sequential_xyz_motion():
    """X, Y, and Z must complete in sequence."""
    fsm = GantryFSM()

    initialize_to_ready(fsm)
    prepare_move(fsm)

    for axis in ("X", "Y", "Z"):
        assert fsm.current_axis == axis

        fsm.trigger(E.MOTION_STEP)
        assert fsm.state == S.READING_POSITION

        fsm.trigger(E.POSITION_READ)
        assert fsm.state == S.VERIFYING_POSITION

        fsm.trigger(E.POSITION_WITHIN_TOLERANCE)
        assert fsm.state == S.AXIS_COMPLETE

        if axis != "Z":
            fsm.trigger(E.NEXT_AXIS)
        else:
            fsm.trigger(E.ALL_AXES_COMPLETE)

    assert fsm.state == S.TARGET_REACHED

    fsm.trigger(E.ACKNOWLEDGE_GOAL)
    assert fsm.state == S.READY


def test_position_error_causes_retry():
    """An axis continues when not within tolerance."""
    fsm = GantryFSM()

    initialize_to_ready(fsm)
    prepare_move(fsm)

    fsm.trigger(E.MOTION_STEP)
    fsm.trigger(E.POSITION_READ)
    fsm.trigger(E.POSITION_ERROR_HIGH)

    assert fsm.state == S.MOVING_TO_TARGET
    assert fsm.current_axis == "X"


def test_initialization_failure():
    """Failed initialization enters FAULT."""
    fsm = GantryFSM()

    fsm.trigger(E.POWER_ON)
    fsm.trigger(E.INITIALIZATION_FAILED)

    assert fsm.state == S.FAULT


def test_estop():
    """An E-stop event disables the FSM."""
    fsm = GantryFSM()

    initialize_to_ready(fsm)
    fsm.trigger(E.ESTOP_ACTIVE)

    assert fsm.state == S.DISABLED

    with pytest.raises(InvalidTransition):
        fsm.trigger(E.COMMAND_RECEIVED)


def test_homing_failure():
    """Failed homing enters FAULT."""
    fsm = GantryFSM()

    for event in (
        E.POWER_ON,
        E.INITIALIZATION_OK,
        E.ESTOP_CLEAR,
        E.HOME_REQUIRED,
        E.HOMING_FAILED,
    ):
        fsm.trigger(event)

    assert fsm.state == S.FAULT


@pytest.mark.parametrize(
    "result, checkpoint",
    [
        (E.COMMAND_INVALID, S.VALIDATING_COMMAND),
        (E.LIMITS_EXCEEDED, S.CHECKING_LIMITS),
        (E.PATH_UNSAFE, S.CHECKING_PATH),
    ],
)
def test_rejected_commands(result, checkpoint):
    """Invalid, out-of-range and unsafe requests are rejected."""
    fsm = GantryFSM()

    initialize_to_ready(fsm)

    fsm.trigger(E.COMMAND_RECEIVED)

    if checkpoint == S.CHECKING_LIMITS:
        fsm.trigger(E.COMMAND_VALID)

    if checkpoint == S.CHECKING_PATH:
        fsm.trigger(E.COMMAND_VALID)
        fsm.trigger(E.LIMITS_OK)

    assert fsm.state == checkpoint

    fsm.trigger(result)
    assert fsm.state == S.READY


def test_fault_reset():
    """Reset returns the FSM to initialization."""
    fsm = GantryFSM()

    initialize_to_ready(fsm)
    fsm.trigger(E.MOTION_FAULT)

    assert fsm.state == S.FAULT

    fsm.trigger(E.RESET)
    assert fsm.state == S.INITIALIZING


def test_invalid_transition():
    """Commands cannot bypass initialization."""
    fsm = GantryFSM()

    with pytest.raises(InvalidTransition):
        fsm.trigger(E.COMMAND_RECEIVED)


def test_cannot_skip_axes():
    """All axes cannot complete while X is active."""
    fsm = GantryFSM()

    initialize_to_ready(fsm)
    prepare_move(fsm)

    fsm.trigger(E.MOTION_STEP)
    fsm.trigger(E.POSITION_READ)
    fsm.trigger(E.POSITION_WITHIN_TOLERANCE)

    with pytest.raises(InvalidTransition):
        fsm.trigger(E.ALL_AXES_COMPLETE)
