
from unittest import mock
from unittest.mock import patch

import pytest

from systematic_files.mounts import Mountpoints, FilesystemError


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


def test_invalid_mountpoints_system_platform():
    """
    Test loading mountpoints with innvalid system platform
    """
    with mock.patch('sys.platform', 'unknown'):
        with pytest.raises(ValueError):
            Mountpoints()


@patch('systematic_files.mounts.detect_platform_family', mock_detect_platform_family)
def test_invalid_mountpoints_platform():
    """
    Test loading mountpoints with invalid response from family detection
    """
    with pytest.raises(FilesystemError):
        Mountpoints()


@patch('systematic_files.mounts.detect_toolchain_family', mock_detect_toolchain_family)
def test_invalid_mountpoints_toolchain():
    """
    Test loading mountpoints with invalid response from toolchain detection
    """
    with pytest.raises(FilesystemError):
        Mountpoints()
