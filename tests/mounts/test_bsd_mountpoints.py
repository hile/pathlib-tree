"""
Unit tests for BSD mountpoints
"""

from pathlib_tree.mounts.platform.bsd import (
    BSDMountpoint,
    BSD_VIRTUAL_FILESYSTEMS
)

from . import MountpointTestCase


class FreeBSDMountPoints(MountpointTestCase):
    """
    Test listing FreeBSD mountpoints
    """
    platform = 'freebsd12'
    mock_platform = 'bsd'
    mock_toolchain = 'bsd'
    mountpoint_class = BSDMountpoint
    virtual_filesystems = BSD_VIRTUAL_FILESYSTEMS

    def test_freebsd_mountpoints_loading(self):
        """
        Test loading mountpoints from mock data for FreeBSD
        """
        mountpoints = self.load_mocked_mountpoints()
        self.verify_mocked_mountpoints(mountpoints)

    def test_lazy_loading(self):
        """
        Verify lazy loading functions
        """
        self.verify_lazy_loading()
