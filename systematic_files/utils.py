"""
Utilities for systematic_files
"""

import os


def current_umask():
    """
    Get currently applied umask
    """
    value = os.umask(0)
    os.umask(value)
    return value
