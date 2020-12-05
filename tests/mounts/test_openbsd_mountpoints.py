"""
Unit tests for OpenBSD mountpoints
"""

from pathlib_tree.mounts.platform.openbsd import (
    OpenBSDMountPoint,
    OPENBSD_VIRTUAL_FILESYSTEMS
)

from . import MountpointTestCase


class OpenBSDMountPoints(MountpointTestCase):
    """
    Test listing OpenBSD mountpoints
    """
    platform = 'openbsd6'
    mock_platform = 'openbsd'
    mock_toolchain = 'openbsd'
    mountpoint_class = OpenBSDMountPoint
    virtual_filesystems = OPENBSD_VIRTUAL_FILESYSTEMS

    def test_freebsd_mountpoints_loading(self):
        """
        Test loading mountpoints from mock data for OpenBSD
        """
        mountpoints = self.load_mocked_mountpoints()
        self.verify_mocked_mountpoints(mountpoints)

    def test_lazy_loading(self):
        """
        Verify lazy loading functions
        """
        self.verify_lazy_loading()
