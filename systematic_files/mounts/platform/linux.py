
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


class LinuxMountpointUsage(MountpointUsage):  # pylint: disable=R0903
    """
    Linux specific mountpoint usage data
    """


class LinuxMountPointOptions(MountpointOptions):  # pylint: disable=R0903
    """
    Linux specific mountpoint options
    """


class LinuxFilesystem(Filesystem):  # pylint: disable=R0903
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
