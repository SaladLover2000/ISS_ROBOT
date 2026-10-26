
"""Validate XYZ coordinate commands for the ISS gantry."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class XYZGoal:
    x: float
    y: float
    z: float


class CommandError(ValueError):
    """Invalid coordinate command."""


def validate_command(values):
    """Return a validated XYZ target in meters."""

    if not isinstance(values, (list, tuple)):
        raise CommandError("Command must be a list or tuple")

    if len(values) != 3:
        raise CommandError("Expected exactly X, Y, Z")

    if any(
        isinstance(v, bool) or not isinstance(v, (int, float))
        for v in values
    ):
        raise CommandError("Coordinates must be numeric")

    if not all(math.isfinite(v) for v in values):
        raise CommandError("Coordinates must be finite")

    return XYZGoal(
        x=float(values[0]),
        y=float(values[1]),
        z=float(values[2]),
    )
