
"""Tests for XYZ validation and path safety."""

import math
import pytest

from iss_coordinate_control.validation.command_validator import (
    XYZGoal,
    CommandError,
    validate_command,
)
from iss_coordinate_control.validation.travel_limits import (
    AxisLimits,
    GantryLimits,
    within_travel_limits,
)
from iss_coordinate_control.validation.path_safety import (
    PathAssessment,
    path_is_safe,
)


# Test-only limits, not real gantry dimensions.
LIMITS = GantryLimits(
    x=AxisLimits(-1.0, 1.0),
    y=AxisLimits(-1.0, 1.0),
    z=AxisLimits(0.0, 1.0),
)


def test_valid_command():
    goal = validate_command((0.2, 0.4, 0.1))
    assert goal == XYZGoal(0.2, 0.4, 0.1)


def test_missing_axis():
    with pytest.raises(CommandError):
        validate_command((0.2, 0.4))


def test_non_numeric_command():
    with pytest.raises(CommandError):
        validate_command(("left", 0.4, 0.1))


def test_nan_rejected():
    with pytest.raises(CommandError):
        validate_command((math.nan, 0.4, 0.1))


def test_in_range():
    assert within_travel_limits(
        XYZGoal(0.2, 0.4, 0.1), LIMITS
    )


def test_out_of_range():
    assert not within_travel_limits(
        XYZGoal(2.0, 0.4, 0.1), LIMITS
    )


def test_invalid_limits():
    with pytest.raises(ValueError):
        AxisLimits(1.0, -1.0)


def test_safe_path():
    assessment = PathAssessment(True, True, True)
    assert path_is_safe(assessment)


def test_unsafe_path():
    assessment = PathAssessment(False, True, True)
    assert not path_is_safe(assessment)


def test_unknown_path_rejected():
    assert not path_is_safe(None)
