"""
Mountpoints loader main class MountPoints()
"""

import re

from cli_toolkit.platform import detect_platform_family, detect_toolchain_family
from cli_toolkit.process import run_command

from ..exceptions import FilesystemError
from .platform.base import Mountpoint
from .platform.bsd import BSDMountpoint
from .platform.darwin import DarwinMountPoint
from .platform.linux import LinuxMountPoint
from .platform.openbsd import OpenBSDMountPoint


from .constants import (
    GNU_MOUNT_COMMAND,
    GNU_DF_COMMAND,
    BSD_MOUNT_COMMAND,
    BSD_DF_COMMAND,
    RE_GNU_MOUNT_LINE,
    RE_GNU_DF_LINE,
    RE_BSD_MOUNT_LINE,
    RE_BSD_DF_LINE,
)


class Mountpoints(list):
    """
    Filesystem mount points with usage
    """
    __mount_command__ = None
    __df_command__ = None
    __re_mount_patterns__ = None
    __re_df_patterns__ = None

    def __init__(self):
        super().__init__()
        self.__platform__ = detect_platform_family()
        self.__toolchain__ = detect_toolchain_family()
        self.__detect_mountpoint_class__()
        self.__initialize_toolchain_based_data__()
        self.__loaded__ = False
        self.__index___ = None

    def __len__(self):
        if not self.__loaded__:
            self.update()
        return super().__len__()

    def __getitem__(self, index):
        if not self.__loaded__:
            self.update()
        return super().__getitem__(index)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Iterate over lazy loaded mountpoints
        """
        if not self.__loaded__:
            self.update()

        if self.__index___ is None:
            self.__index___ = 0

        try:
            mountpoint = self[self.__index___]
            self.__index___ += 1
            return mountpoint
        except IndexError as error:
            self.__index___ = None
            raise StopIteration from error

    def __detect_mountpoint_class__(self):
        """
        Detect mountpoint loader class based on platform family
        """
        if self.__platform__ == 'bsd':
            self.__mountpoint_class__ = BSDMountpoint
        elif self.__platform__ == 'darwin':
            self.__mountpoint_class__ = DarwinMountPoint
        elif self.__platform__ == 'linux':
            self.__mountpoint_class__ = LinuxMountPoint
        elif self.__platform__ == 'openbsd':
            self.__mountpoint_class__ = OpenBSDMountPoint
        else:
            raise FilesystemError(f'Unsupported OS platform: {self.__platform__}')

    def __initialize_toolchain_based_data__(self):
        """
        Initialize toolchain specific commands and regexp patterns
        """
        if self.__toolchain__ == 'bsd':
            self.__mount_command__ = BSD_MOUNT_COMMAND
            self.__df_command__ = BSD_DF_COMMAND
            self.__re_mount_patterns__ = RE_BSD_MOUNT_LINE
            self.__re_df_patterns__ = RE_BSD_DF_LINE

        elif self.__toolchain__ in ('gnu', 'openbsd'):
            self.__mount_command__ = GNU_MOUNT_COMMAND
            self.__df_command__ = GNU_DF_COMMAND
            self.__re_mount_patterns__ = RE_GNU_MOUNT_LINE
            self.__re_df_patterns__ = RE_GNU_DF_LINE

        else:
            raise FilesystemError(f'Unexpected toolchain detected: {self.__toolchain__}')

    @staticmethod
    def __match_pattern_list__(lines, patterns):
        """
        Match lines to list of grouped regexp patterns, returning list
        of regexp groupdict matches.

        Lines must be iterable of strings and iterable of re.Pattern
        """
        assert isinstance(patterns, list)
        for pattern in patterns:
            assert isinstance(pattern, re.Pattern)
        matches = []
        for line in lines:
            assert isinstance(line, str)
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    matches.append(match.groupdict())
                    break
        return matches

    def __get_mount_lines__(self):
        """
        Return lines from mount command
        """
        stdout, _stderr = run_command(*self.__mount_command__)
        return [str(line, 'utf-8') for line in stdout.splitlines()]

    def __get_df_lines__(self):
        """
        Return lines from df command
        """
        stdout, _stderr = run_command(*self.__df_command__)
        return [str(line, 'utf-8') for line in stdout.splitlines()]

    def __get_mountpoint_data__(self, lines):
        """
        Return lines from mount command
        """
        return self.__match_pattern_list__(lines, self.__re_mount_patterns__)

    def __get_df_data__(self, lines):
        """
        Return lines from df command
        """
        return self.__match_pattern_list__(lines, self.__re_df_patterns__)

    def append(self, value):
        assert isinstance(value, Mountpoint)
        if not self.__loaded__:
            self.update()
        return super().append(value)

    def insert(self, index, value):
        assert isinstance(value, Mountpoint)
        if not self.__loaded__:
            self.update()
        return super().insert(index, value)

    def update(self):
        """
        Get data for mountpoints
        """
        self.__loaded__ = True

        del self[0:len(self)]
        mountpoints = {}
        for match in self.__get_mountpoint_data__(self.__get_mount_lines__()):
            item = self.__mountpoint_class__(self, **match)
            mountpoints[item.mountpoint] = item
            self.append(item)

        for match in self.__get_df_data__(self.__get_df_lines__()):
            item = mountpoints.get(match['mountpoint'], None)
            if item is not None:
                item.load_usage_data(match)
