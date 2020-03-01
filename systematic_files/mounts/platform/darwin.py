
from .bsd import BSDMountpoint, BSDFilesystem, BSDMountPointOptions, BSDMountpointUsage

DARWIN_VIRTUAL_FILESYSTEMS = (
    'sysfs',
)


class DarwinMountpointUsage(BSDMountpointUsage):  # pylint: disable=R0903
    """
    MacOS darwin specific mountpoint usage data
    """


class DarwinMountPointOptions(BSDMountPointOptions):  # pylint: disable=R0903
    """
    MacOS darwin specific mountpoint options
    """


class DarwinFilesystem(BSDFilesystem):  # pylint: disable=R0903
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
