"""
Linux mountpoints
"""
from .base import Mountpoint, Filesystem, MountpointOptions, MountpointUsage

LINUX_VIRTUAL_FILESYSTEMS = (
    'proc',
    'sysfs',
    'cgroup',
    'autofs',
    'hugetlbfs',
    'mqueue',
    'devpts',
    'devtmpfs',
    'tmpfs',
    'fusectl',
    'pstore',
    'configfs',
    'selinuxfs',
    'securityfs',
    'debugfs',
    'rpc_pipefs',
    'binfmt_misc',
    'nfsd',
    'fuse.vmware-vmblock',
)


# pylint: disable=too-few-public-methods
class LinuxMountpointUsage(MountpointUsage):
    """
    Linux specific mountpoint usage data
    """


# pylint: disable=too-few-public-methods
class LinuxMountPointOptions(MountpointOptions):
    """
    Linux specific mountpoint options
    """


# pylint: disable=too-few-public-methods
class LinuxFilesystem(Filesystem):
    """
    Linux specific mountpoint options
    """
    virtual_filesystems = LINUX_VIRTUAL_FILESYSTEMS


class LinuxMountPoint(Mountpoint):
    """
    Linux specific mountpoint
    """
    filesystem_class = LinuxFilesystem
    options_class = LinuxMountPointOptions
    usage_class = LinuxMountpointUsage
