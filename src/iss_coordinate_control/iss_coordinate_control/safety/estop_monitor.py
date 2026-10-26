
"""Emergency-stop status monitoring for the gantry."""


class EStopMonitor:
    """Maintain a fail-closed emergency-stop status."""

    def __init__(self):
        # None means status is unknown.
        self._active = None

    def update(self, active: bool):
        """Accept a verified E-stop signal."""
        if type(active) is not bool:
            raise TypeError("E-stop status must be a boolean")

        self._active = active

    @property
    def active(self):
        """Return True for active or unknown status."""
        return self._active is not False

    @property
    def known(self):
        """Report whether a valid status was received."""
        return self._active is not None

    @property
    def motion_permitted(self):
        """Permit motion only when explicitly cleared."""
        return self._active is False
