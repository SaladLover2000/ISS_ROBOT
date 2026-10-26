
"""Cartesian travel-limit checks."""

from dataclasses import dataclass
import math

from .command_validator import XYZGoal


@dataclass(frozen=True)
class AxisLimits:
    minimum: float
    maximum: float

    def __post_init__(self):
        if not (
            math.isfinite(self.minimum)
            and math.isfinite(self.maximum)
            and self.minimum <= self.maximum
        ):
            raise ValueError("Invalid axis limits")

    def contains(self, value):
        return self.minimum <= value <= self.maximum


@dataclass(frozen=True)
class GantryLimits:
    x: AxisLimits
    y: AxisLimits
    z: AxisLimits


def within_travel_limits(goal: XYZGoal, limits: GantryLimits):
    """Check all three Cartesian ranges."""
    return (
        limits.x.contains(goal.x)
        and limits.y.contains(goal.y)
        and limits.z.contains(goal.z)
    )
