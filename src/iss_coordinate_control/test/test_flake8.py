
"""Check Python code style with flake8."""

import pytest


@pytest.mark.linter
@pytest.mark.flake8
def test_flake8():
    """Check Python files for style errors."""
    pytest.importorskip("ament_flake8")
    from ament_flake8.main import main_with_errors

    return_code, errors = main_with_errors(argv=[])

    assert return_code == 0, (
        "Code style errors:\n" + "\n".join(errors)
    )
