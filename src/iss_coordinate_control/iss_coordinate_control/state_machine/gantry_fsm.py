
"""Supervisory finite state machine for the ISS XYZ gantry."""

from .states import GantryEvent as E
from .states import GantryState as S


class InvalidTransition(Exception):
    """An event is not permitted in the current state."""


class GantryFSM:
    """Manage gantry states and sequential XYZ operations."""

    AXES = ("X", "Y", "Z")

    TRANSITIONS = {
        # Startup and system initialization
        (S.STARTUP, E.POWER_ON): S.INITIALIZING,
        (S.INITIALIZING, E.INITIALIZATION_OK):
            S.CHECKING_ESTOP,
        (S.INITIALIZING, E.INITIALIZATION_FAILED):
            S.FAULT,

        # E-stop check
        (S.CHECKING_ESTOP, E.ESTOP_CLEAR):
            S.CHECKING_HOME,
        (S.CHECKING_ESTOP, E.ESTOP_ACTIVE):
            S.DISABLED,

        # Homing check and homing sequence
        (S.CHECKING_HOME, E.ALREADY_HOMED):
            S.READY,
        (S.CHECKING_HOME, E.HOME_REQUIRED):
            S.HOMING,
        (S.HOMING, E.HOMING_SUCCEEDED):
            S.READY,
        (S.HOMING, E.HOMING_FAILED):
            S.FAULT,

        # Receive a target XYZ command
        (S.READY, E.COMMAND_RECEIVED):
            S.VALIDATING_COMMAND,

        # Check command format
        (S.VALIDATING_COMMAND, E.COMMAND_VALID):
            S.CHECKING_LIMITS,
        (S.VALIDATING_COMMAND, E.COMMAND_INVALID):
            S.READY,

        # Check mechanical travel limits
        (S.CHECKING_LIMITS, E.LIMITS_OK):
            S.CHECKING_PATH,
        (S.CHECKING_LIMITS, E.LIMITS_EXCEEDED):
            S.READY,

        # Check target and path safety
        (S.CHECKING_PATH, E.PATH_SAFE):
            S.MOVING_TO_TARGET,
        (S.CHECKING_PATH, E.PATH_UNSAFE):
            S.READY,

        # Axis motion and feedback loop
        (S.MOVING_TO_TARGET, E.MOTION_STEP):
            S.READING_POSITION,
        (S.READING_POSITION, E.POSITION_READ):
            S.VERIFYING_POSITION,
        (S.VERIFYING_POSITION, E.POSITION_ERROR_HIGH):
            S.MOVING_TO_TARGET,
        (S.VERIFYING_POSITION,
         E.POSITION_WITHIN_TOLERANCE):
            S.AXIS_COMPLETE,

        # Sequential X -> Y -> Z progression
        (S.AXIS_COMPLETE, E.NEXT_AXIS):
            S.MOVING_TO_TARGET,
        (S.AXIS_COMPLETE, E.ALL_AXES_COMPLETE):
            S.TARGET_REACHED,

        # Completion
        (S.TARGET_REACHED, E.ACKNOWLEDGE_GOAL):
            S.READY,

        # Recovery requires reinitialization
        (S.FAULT, E.RESET):
            S.INITIALIZING,
        (S.DISABLED, E.RESET):
            S.INITIALIZING,
    }

    def __init__(self):
        """Initialize the state machine."""
        self.state = S.STARTUP
        self.axis_index = 0
        self.last_event = None
        self.history = []

    @property
    def current_axis(self):
        """Return the axis currently being controlled."""
        return self.AXES[self.axis_index]

    def trigger(self, event):
        """Process an event and update the FSM state."""

        if not isinstance(event, E):
            raise TypeError("Expected a GantryEvent")

        # E-stop overrides normal operating transitions.
        if event == E.ESTOP_ACTIVE:
            self.axis_index = 0
            return self._transition(event, S.DISABLED)

        # Motion faults override normal operating transitions.
        if event == E.MOTION_FAULT:
            self.axis_index = 0
            return self._transition(event, S.FAULT)

        key = (self.state, event)

        if key not in self.TRANSITIONS:
            raise InvalidTransition(
                f"{event.name} is invalid in "
                f"state {self.state.name}"
            )

        if event == E.NEXT_AXIS:
            if self.axis_index >= len(self.AXES) - 1:
                raise InvalidTransition(
                    "Cannot advance beyond Z"
                )

        if event == E.ALL_AXES_COMPLETE:
            if self.axis_index != len(self.AXES) - 1:
                raise InvalidTransition(
                    "X, Y, and Z have not all completed"
                )

        new_state = self.TRANSITIONS[key]

        # Reset axis index for a new trajectory.
        if event == E.PATH_SAFE:
            self.axis_index = 0

        elif event == E.NEXT_AXIS:
            self.axis_index += 1

        elif event in (
            E.RESET,
            E.ACKNOWLEDGE_GOAL,
        ):
            self.axis_index = 0

        return self._transition(event, new_state)

    def _transition(self, event, new_state):
        """Record a state transition."""
        old_state = self.state

        self.state = new_state
        self.last_event = event

        self.history.append(
            (old_state, event, new_state)
        )

        return self.state

    def get_status(self):
        """Return a status dictionary."""
        return {
            "state": self.state.name,
            "current_axis": self.current_axis,
            "last_event": (
                self.last_event.name
                if self.last_event is not None
                else None
            ),
        }
