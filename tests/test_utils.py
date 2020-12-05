"""
Unit tests for pathlib_tree.utils umask functions
"""

from pathlib_tree.utils import current_umask


def validate_umask(umask):
    """
    Validate umask value
    """
    assert isinstance(umask, int)
    assert 0 <= umask <= 511


def test_current_umask():
    """
    Test retrieving current value for umask
    """
    umask = current_umask()
    validate_umask(umask)
