
"""States and events for the ISS XYZ gantry state machine."""

from enum import Enum, auto


class GantryState(Enum):
    """Operational states of the gantry."""

    STARTUP = auto()
    INITIALIZING = auto()
    CHECKING_ESTOP = auto()
    CHECKING_HOME = auto()
    HOMING = auto()

    READY = auto()
    VALIDATING_COMMAND = auto()
    CHECKING_LIMITS = auto()
    CHECKING_PATH = auto()

    MOVING_TO_TARGET = auto()
    READING_POSITION = auto()
    VERIFYING_POSITION = auto()
    AXIS_COMPLETE = auto()
    TARGET_REACHED = auto()

    DISABLED = auto()
    FAULT = auto()


class GantryEvent(Enum):
    """Events that cause a state transition."""

    POWER_ON = auto()

    INITIALIZATION_OK = auto()
    INITIALIZATION_FAILED = auto()

    ESTOP_CLEAR = auto()
    ESTOP_ACTIVE = auto()

    ALREADY_HOMED = auto()
    HOME_REQUIRED = auto()
    HOMING_SUCCEEDED = auto()
    HOMING_FAILED = auto()

    COMMAND_RECEIVED = auto()
    COMMAND_VALID = auto()
    COMMAND_INVALID = auto()

    LIMITS_OK = auto()
    LIMITS_EXCEEDED = auto()

    PATH_SAFE = auto()
    PATH_UNSAFE = auto()

    MOTION_STEP = auto()
    POSITION_READ = auto()
    POSITION_ERROR_HIGH = auto()
    POSITION_WITHIN_TOLERANCE = auto()

    NEXT_AXIS = auto()
    ALL_AXES_COMPLETE = auto()
    ACKNOWLEDGE_GOAL = auto()

    MOTION_FAULT = auto()
    RESET = auto()
