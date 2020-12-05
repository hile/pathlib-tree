"""
Unit tests for unknown platform mountpoints
"""

import pytest

from pathlib_tree.exceptions import FilesystemError
from pathlib_tree.mounts import Mountpoints


def mock_detect_platform_family():
    """
    Callback to mock platform family detection
    """
    return 'test'


def mock_detect_toolchain_family():
    """
    Callback to mock toolchain detection
    """
    return 'test'


def test_invalid_mountpoints_system_platform(monkeypatch):
    """
    Test loading mountpoints with innvalid system platform
    """
    monkeypatch.setattr('sys.platform', 'unknown')
    with pytest.raises(ValueError):
        Mountpoints()


def test_invalid_mountpoints_platform(monkeypatch):
    """
    Test loading mountpoints with invalid response from family detection
    """
    monkeypatch.setattr(
        'pathlib_tree.mounts.loader.detect_platform_family',
        mock_detect_platform_family,
    )
    with pytest.raises(FilesystemError):
        Mountpoints()


def test_invalid_mountpoints_toolchain(monkeypatch):
    """
    Test loading mountpoints with invalid response from toolchain detection
    """
    monkeypatch.setattr(
        'pathlib_tree.mounts.loader.detect_toolchain_family',
        mock_detect_toolchain_family
    )
    with pytest.raises(FilesystemError):
        Mountpoints()
