
from .bsd import BSDMountpoint, BSDFilesystem, BSDMountPointOptions, BSDMountpointUsage

OPENBSD_VIRTUAL_FILESYSTEMS = (
    'sysfs',
    'procfs',
)


class OpenBSDMountpointUsage(BSDMountpointUsage):  # pylint: disable=R0903
    """
    OpenBSD specific mountpoint usage data
    """


class OpenBSDMountPointOptions(BSDMountPointOptions):  # pylint: disable=R0903
    """
    OpenBSD specific mountpoint options
    """


class OpenBSDFilesystem(BSDFilesystem):  # pylint: disable=R0903
    """
    OpenBSD specific mountpoint options
    """
    virtual_filesystems = OPENBSD_VIRTUAL_FILESYSTEMS


class OpenBSDMountPoint(BSDMountpoint):
    """
    OpenBSD specific mountpoint
    """
    filesystem_class = OpenBSDFilesystem
    options_class = OpenBSDMountPointOptions
    usage_class = OpenBSDMountpointUsage
