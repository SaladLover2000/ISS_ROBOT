
"""Conservative path-clearance checks for gantry motion."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PathAssessment:
    """Result supplied by a trajectory safety checker."""

    collision_free: bool
    mechanically_reachable: bool
    feedback_valid: bool


def path_is_safe(assessment: PathAssessment | None):
    """Reject missing, incomplete, or unsafe assessments."""
    if assessment is None:
        return False

    if not isinstance(assessment, PathAssessment):
        return False

    return (
        assessment.collision_free is True
        and assessment.mechanically_reachable is True
        and assessment.feedback_valid is True
    )
