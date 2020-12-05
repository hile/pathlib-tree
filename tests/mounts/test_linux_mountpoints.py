"""
Unit tests for linux mountpoints
"""

from pathlib_tree.mounts.platform.linux import (
    LinuxMountPoint,
    LINUX_VIRTUAL_FILESYSTEMS
)

from . import MountpointTestCase


class LinuxDMountPoints(MountpointTestCase):
    """
    Test listing FreeBSD mountpoints
    """
    platform = 'linux'
    mock_platform = 'linux'
    mock_toolchain = 'gnu'
    mountpoint_class = LinuxMountPoint
    virtual_filesystems = LINUX_VIRTUAL_FILESYSTEMS

    def test_linux_mountpoints_loading(self):
        """
        Test loading mountpoints from mock data for Linux
        """
        mountpoints = self.load_mocked_mountpoints()
        self.verify_mocked_mountpoints(mountpoints)

    def test_lazy_loading(self):
        """
        Verify lazy loading functions
        """
        self.verify_lazy_loading()
