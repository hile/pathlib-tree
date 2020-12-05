
from pathlib import Path


# pylint: disable=too-few-public-methods
class MountpointOptions:
    """
    Options for filesystem mount point
    """
    def __init__(self, mountpoint, options=None):
        self.mountpoint = mountpoint

        if options is None:
            return

        options = self.__parse_options__(options)
        for flag in options:
            setattr(self, flag, True)

    @staticmethod
    def __parse_options__(options):
        """
        Parse options from string to a list
        """
        if isinstance(options, str):
            options = options.split(', ')
        return options


# pylint: disable=too-few-public-methods
class MountpointUsage:
    """

    Mountpoint usage stats data
    """
    def __init__(self, mountpoint):
        self.mountpoint = mountpoint
        self.size = None
        self.available = None
        self.used = None
        self.percent = None

    def __set_value__(self, attr, value):
        """
        Set value for usage counter
        """
        assert value is not None
        value = int(value)
        setattr(self, attr, value)

    def load_data(self, data):
        """
        Load usage data for mountpoint
        """
        assert isinstance(data, dict)
        for attr in ('size', 'available', 'used', 'percent'):
            assert attr in data
            self.__set_value__(attr, data[attr])


# pylint: disable=too-few-public-methods
class Filesystem:
    """
    Filesystem for a mountpoint
    """
    virtual_filesystems = ()

    def __init__(self, mountpoint, name):
        self.mountpoint = mountpoint
        self.name = name

    def __repr__(self):
        return self.name

    @property
    def is_virtual(self):
        """
        Return True if filesystem is a virtual filesystem
        """
        return self.name in self.virtual_filesystems


class Mountpoint:
    """
    Filesystem mount point linked to Mountpoints
    """
    filesystem_class = Filesystem
    options_class = MountpointOptions
    usage_class = MountpointUsage

    def __init__(self,
                 mountpoints,
                 device,
                 mountpoint,
                 filesystem=None,
                 options=None):

        self.mountpoints = mountpoints
        self.device = device
        self.mountpoint = mountpoint
        self.filesystem = self.filesystem_class(self, filesystem)
        self.options = self.options_class(self, options)
        self.usage = self.usage_class(self)

    def __repr__(self):
        return f'{self.device} mounted on {self.mountpoint}'

    @property
    def name(self):
        """
        Return basename of mountpoint
        """
        return Path(self.mountpoint).name

    @property
    def is_virtual(self):
        """
        Check if filesystem is virtual
        """
        return self.filesystem.is_virtual

    def load_usage_data(self, data):
        """
        Load filesystem usage data for mountpoint
        """
        self.usage.load_data(data)
