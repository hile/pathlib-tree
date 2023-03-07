#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Utilities for pathlib_tree
"""
import os


def current_umask() -> int:
    """
    Get currently applied umask
    """
    value = os.umask(0)
    os.umask(value)
    return value
