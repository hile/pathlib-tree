"""
Unit tests for loading mount points for various platforms
"""

import unittest

from pathlib import Path
from unittest import mock

from pathlib_tree.mounts import Mountpoints
from pathlib_tree.mounts.platform.base import Mountpoint


class MountpointTestCase(unittest.TestCase):
    """
    Common base class for mountpoint unit tests
    """
    platform = None
    mock_platform = None
    mock_toolchain = None
    mountpoint_class = Mountpoint
    virtual_filesystems = []

    def load_mount_data(self):
        """
        Load data file with fake mount command output
        """
        datafile = Path(__file__).absolute().parent.joinpath('data', self.platform, 'mount')
        with open(datafile, 'r') as filedescriptor:
            return filedescriptor.readlines()

    def load_df_data(self):
        """
        Load data file with fake df command output
        """
        datafile = Path(__file__).absolute().parent.joinpath('data', self.platform, 'df')
        with open(datafile, 'r') as filedescriptor:
            return filedescriptor.readlines()

    def setUp(self):
        """
        Setup mountpoint test case with command output data from mock files
        """
        sys = mock.MagicMock()
        sys.configure_mock(platform=self.platform)

    def load_mocked_mountpoints(self):
        """
        Load mountpoint data with mocked
        """
        with mock.patch('sys.platform', self.platform):
            mountpoints = Mountpoints()
            mountpoints.__get_mount_lines__ = self.load_mount_data
            mountpoints.__get_df_lines__ = self.load_df_data

        return mountpoints

    def create_fake_mountpoint(self, mountpoints):
        """
        Create a mountpoint item for update tests
        """
        return self.mountpoint_class(
            mountpoints=mountpoints,
            device='/dev/test',
            mountpoint='/unittest',
        )

    def verify_lazy_len(self):
        """
        Ensure lazy __len__ call updates data
        """
        mountpoints = self.load_mocked_mountpoints()

        assert mountpoints.__loaded__ is False
        assert len(mountpoints) > 0
        assert mountpoints.__loaded__ is True

    def verify_lazy_getitem(self):
        """
        Ensure lazy __len__ call updates data
        """
        mountpoints = self.load_mocked_mountpoints()

        assert mountpoints.__loaded__ is False
        item = mountpoints[0]
        assert mountpoints.__loaded__ is True
        assert isinstance(item, Mountpoint)

    def verify_lazy_next(self):
        """
        Ensure lazy __next__ call updates data
        """
        mountpoints = self.load_mocked_mountpoints()

        assert mountpoints.__loaded__ is False
        item = next(mountpoints)
        assert mountpoints.__loaded__ is True
        assert isinstance(item, Mountpoint)

    def verify_lazy_set(self):
        """
        Ensure lazy insert call updates data and adds item to specified index
        """
        mountpoints = self.load_mocked_mountpoints()
        mountpoint = self.create_fake_mountpoint(mountpoints)

        assert mountpoints.__loaded__ is False
        mountpoints[1] = mountpoint
        assert mountpoints.__loaded__ is True
        assert mountpoints[1] == mountpoint
        mountpoints[-1] = mountpoint

    def verify_lazy_insert(self):
        """
        Ensure lazy insert call updates data and adds item to specified index
        """
        mountpoints = self.load_mocked_mountpoints()
        mountpoint = self.create_fake_mountpoint(mountpoints)

        assert mountpoints.__loaded__ is False
        mountpoints.insert(1, mountpoint)
        assert mountpoints.__loaded__ is True
        assert mountpoints[1] == mountpoint
        mountpoints.insert(1, mountpoint)

    def verify_lazy_delete(self):
        """
        Ensure lazy insert call updates data and adds item to specified index
        """
        mountpoints = self.load_mocked_mountpoints()

        assert mountpoints.__loaded__ is False
        del mountpoints[1]
        assert mountpoints.__loaded__ is True
        del mountpoints[-1]

    def verify_lazy_append(self):
        """
        Ensure lazy append call updates data and adds item to end of list
        """
        mountpoints = self.load_mocked_mountpoints()
        mountpoint = self.create_fake_mountpoint(mountpoints)

        assert mountpoints.__loaded__ is False
        mountpoints.append(mountpoint)
        assert mountpoints.__loaded__ is True
        assert mountpoints[-1] == mountpoint

    def verify_lazy_loading(self):
        """
        Verify all lazy loading functions
        """
        self.verify_lazy_len()
        self.verify_lazy_getitem()
        self.verify_lazy_next()
        self.verify_lazy_insert()
        self.verify_lazy_append()

    def verify_mountpoint_filesystem(self, mountpoint):
        """
        Check mountpoint filesystem info
        """
        assert isinstance(mountpoint.__repr__(), str)
        assert isinstance(mountpoint.name, str)
        assert isinstance(mountpoint.filesystem.__repr__(), str)
        assert isinstance(mountpoint.is_virtual, bool)

        assert isinstance(mountpoint.filesystem.name, str)
        assert isinstance(mountpoint.filesystem.is_virtual, bool)

        if mountpoint.filesystem.name in self.virtual_filesystems:
            assert mountpoint.filesystem.is_virtual is True
        else:
            assert mountpoint.filesystem.is_virtual is False

    @staticmethod
    def verify_mountpoint_usage_fields(mountpoint):
        """
        Verify usage details for mountpoint
        """
        counters = ('size', 'used', 'available', 'percent')
        if mountpoint.usage.size is not None:
            for counter in counters:
                value = getattr(mountpoint.usage, counter)
                assert isinstance(value, int)

            assert mountpoint.usage.size >= mountpoint.usage.used
            assert mountpoint.usage.size >= mountpoint.usage.available
            assert mountpoint.usage.percent <= 100

        else:
            for counter in counters:
                assert getattr(mountpoint.usage, counter) is None

    def verify_mocked_mountpoints(self, mountpoints):
        """
        Verify mountpoints match expected platform and family
        """
        assert mountpoints.__platform__ == self.mock_platform
        assert mountpoints.__toolchain__ == self.mock_toolchain
        assert mountpoints.__mountpoint_class__ == self.mountpoint_class

        assert mountpoints.__loaded__ is False
        assert len(mountpoints) > 0
        assert mountpoints.__loaded__ is True

        for mountpoint in mountpoints:
            self.verify_mountpoint_filesystem(mountpoint)
            self.verify_mountpoint_usage_fields(mountpoint)
