"""
Unit tests for MacOS darwin mountpoints
"""

from pathlib_tree.mounts.platform.darwin import (
    DarwinMountPoint,
    DARWIN_VIRTUAL_FILESYSTEMS
)

from . import MountpointTestCase


class DarwinMountPoints(MountpointTestCase):
    """
    Test listing darwin mountpoints
    """
    platform = 'darwin'
    mock_platform = 'darwin'
    mock_toolchain = 'bsd'
    mountpoint_class = DarwinMountPoint
    virtual_filesystems = DARWIN_VIRTUAL_FILESYSTEMS

    def test_darwin_mountpoints_loading(self):
        """
        Test loading mountpoints from mock data for MacOS darwin
        """
        mountpoints = self.load_mocked_mountpoints()
        self.verify_mocked_mountpoints(mountpoints)

    def test_lazy_loading(self):
        """
        Verify lazy loading functions
        """
        self.verify_lazy_loading()
