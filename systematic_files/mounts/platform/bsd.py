"""
Generic BSD mountpoints (FreeBSD, MacOS)
"""

from .base import Mountpoint, Filesystem, MountpointOptions, MountpointUsage

BSD_VIRTUAL_FILESYSTEMS = (
    'devfs',
    'procfs',
)


# pylint: disable=too-few-public-methods
class BSDMountpointUsage(MountpointUsage):
    """
    BSD specific mountpoint usage data
    """
    def __init__(self, mountpoint):
        super().__init__(mountpoint)
        self.inodes_used = None
        self.inodes_available = None
        self.inodes_percent = None

    def load_data(self, data):
        """
        Load BSD specific filesystem usage data
        """
        super().load_data(data)
        for attr in ('inodes_used', 'inodes_available', 'inodes_percent'):
            if attr in data:
                self.__set_value__(attr, data[attr])


# pylint: disable=too-few-public-methods
class BSDMountPointOptions(MountpointOptions):
    """
    BSD specific mountpoint options
    """
    def __init__(self, mountpoint, options=None):
        options = self.__parse_options__(options)
        if options is None:
            return
        filesystem = options[0]
        options = options[1:]

        super().__init__(mountpoint, options)
        self.mountpoint.filesystem.name = filesystem


# pylint: disable=too-few-public-methods
class BSDFilesystem(Filesystem):
    """
    BSD specific mountpoint filesystem

    On BSD systems filesystem name comes from options
    """
    virtual_filesystems = BSD_VIRTUAL_FILESYSTEMS


class BSDMountpoint(Mountpoint):
    """
    BSD specific mountpoint
    """
    filesystem_class = BSDFilesystem
    options_class = BSDMountPointOptions
    usage_class = BSDMountpointUsage
