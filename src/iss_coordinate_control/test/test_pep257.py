
"""Check Python documentation style."""

import pytest


@pytest.mark.linter
@pytest.mark.pep257
def test_pep257():
    """Check Python docstrings."""
    pytest.importorskip("ament_pep257")
    from ament_pep257.main import main

    assert main(argv=['.', 'test']) == 0, (
        "Python documentation style errors found"
    )
