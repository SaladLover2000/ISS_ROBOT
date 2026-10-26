
"""Sequential homing supervisor for the ISS XYZ gantry."""


class HomingError(Exception):
    """Invalid homing operation or failed homing step."""


class HomingSequence:
    """Track the required X, Y, Z homing sequence."""

    AXES = ("X", "Y", "Z")

    def __init__(self):
        self.reset()

    def reset(self):
        """Invalidate previous homing and start from X."""
        self.axis_index = 0
        self.completed = []
        self.failed = False

    @property
    def current_axis(self):
        """Return the axis requiring homing."""
        if self.is_homed or self.failed:
            return None
        return self.AXES[self.axis_index]

    @property
    def is_homed(self):
        """True only when all axes are verified."""
        return len(self.completed) == len(self.AXES)

    def confirm_axis(self, axis: str, verified: bool):
        """Process an external homing-verification result."""
        if self.is_homed or self.failed:
            raise HomingError("Homing sequence is not active")

        if axis != self.current_axis:
            raise HomingError(
                f"Expected {self.current_axis}, received {axis}"
            )

        if type(verified) is not bool:
            raise TypeError("Verification must be boolean")

        if not verified:
            self.failed = True
            return False

        self.completed.append(axis)

        if not self.is_homed:
            self.axis_index += 1

        return True

    def get_status(self):
        """Return the homing sequence status."""
        return {
            "current_axis": self.current_axis,
            "completed_axes": list(self.completed),
            "homed": self.is_homed,
            "failed": self.failed,
        }
