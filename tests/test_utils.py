#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for pathlib_tree.utils umask functions
"""
from pathlib_tree.utils import current_umask


def validate_umask(umask: int) -> None:
    """
    Validate umask value
    """
    assert isinstance(umask, int)
    assert 0 <= umask <= 511


def test_current_umask() -> None:
    """
    Test retrieving current value for umask
    """
    umask = current_umask()
    validate_umask(umask)
