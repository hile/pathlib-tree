"""
MacOS Darwin mountpoints
"""

from .bsd import BSDMountpoint, BSDFilesystem, BSDMountPointOptions, BSDMountpointUsage

DARWIN_VIRTUAL_FILESYSTEMS = (
    'sysfs',
)


# pylint: disable=too-few-public-methods
class DarwinMountpointUsage(BSDMountpointUsage):
    """
    MacOS darwin specific mountpoint usage data
    """


# pylint: disable=too-few-public-methods
class DarwinMountPointOptions(BSDMountPointOptions):
    """
    MacOS darwin specific mountpoint options
    """


# pylint: disable=too-few-public-methods
class DarwinFilesystem(BSDFilesystem):
    """
    MacOS darwin specific mountpoint options
    """
    virtual_filesystems = DARWIN_VIRTUAL_FILESYSTEMS


class DarwinMountPoint(BSDMountpoint):
    """
    MacOS darwin specific mountpoint
    """
    filesystem_class = DarwinFilesystem
    options_class = DarwinMountPointOptions
    usage_class = DarwinMountpointUsage
