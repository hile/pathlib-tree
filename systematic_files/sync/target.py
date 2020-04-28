"""
Tree sync target
"""

import os
import pathlib

from tempfile import NamedTemporaryFile

from systematic_cli.file import LineTextFile
from systematic_cli.process import run_command


class SyncError(Exception):
    """
    Exceptions caused by rsync commands
    """


class ExcludesFile(pathlib.Path):
    """
    Rsync excludes parser
    """
    # pylint: disable=protected-access
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    @property
    def excludes(self):
        """
        Return excludes file items
        """
        if self.is_file():
            return list(LineTextFile(self))
        return []


# pylint: disable=too-few-public-methods
class TemporaryExcludesFile:
    """
    A temporary excludes file, merging excludes flags from various
    sources for rsync
    """
    def __init__(self, target):
        self.target = target
        self.__tempfile__ = NamedTemporaryFile(
            mode='w',
            prefix=f'treesync-{self.target.name}'
        )
        for line in self.target.excluded:
            self.__tempfile__.write(f'{line}\n')
        self.__tempfile__.flush()

    def __repr__(self):
        """
        Return path to temporary file
        """
        return self.__tempfile__.name


class Target:
    """
    Tree sync target
    """
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings
        self.__excludes_file__ = None

    def __repr__(self):
        return self.name

    @property
    def default_settings(self):
        """
        Configuration section for target settings
        """
        return self.settings.__parent__.__parent__.defaults

    @property
    def excluded(self):
        """
        Return list of excluded filenames applicable to target
        """
        excluded = list(self.default_settings.never_sync_paths)
        if not self.settings.ignore_default_excludes:
            excluded.extend(self.default_settings.excluded_paths)
        if self.settings.excludes:
            excluded.extend(self.settings.excludes)
        if self.tree_excludes_file is not None:
            excluded.extend(self.tree_excludes_file.excludes)
        return sorted(set(excluded))

    @property
    def tree_excludes_file(self):
        """
        Return tree specific excludes file
        """
        path = self.settings.excludes_file
        if path:
            return ExcludesFile(
                self.source.joinpath(self.settings.excludes_file)
            )
        if self.default_settings.tree_excludes_file:
            return ExcludesFile(
                self.source.joinpath(self.default_settings.tree_excludes_file)
            )
        return None

    @property
    def excludes_file(self):
        """
        Return temporary excludes file for commands
        """
        if self.__excludes_file__ is None:
            self.__excludes_file__ = TemporaryExcludesFile(self)
        return self.__excludes_file__

    @property
    def flags(self):
        """
        Return list of rsync flags for commands
        """
        flags = []
        if not self.settings.ignore_default_excludes:
            flags.extend(list(self.default_settings.flags))
        for flag in self.settings.flags:
            if flag not in flags:
                flags.append(flag)
        if not flags:
            raise ValueError(f'Target defines no rsync flags: {self}')
        if self.settings.iconv:
            flags.append(f'--iconv={self.settings.iconv}')
        flags.append(f'--exclude-from={self.excludes_file}')
        return flags

    @property
    def source(self):
        """
        Return pathlib.Path for source
        """
        return pathlib.Path(self.settings.source)

    @property
    def destination(self):
        """
        Return rsync destination
        """
        return self.settings.destination

    @property
    def rsync_cmd_args(self):
        """
        Return rsync command and arguments excluding source and destination
        """
        return [self.default_settings.rsync_command] + self.flags

    def pull(self):
        """
        Pull data from destination to source with rsync
        """
        args = self.rsync_cmd_args
        args.extend([
            f'{self.destination.rstrip("/")}/',
            f'{str(self.source).rstrip("/")}/',
        ])
        return run_command(*args)

    def push(self):
        """
        Push data from source to destination with rsync
        """
        if not self.source.is_dir():
            raise SyncError(f'Source directory does not exist: {self.source}')
        args = self.rsync_cmd_args
        args.extend([
            f'{str(self.source).rstrip("/")}/',
            f'{self.destination.rstrip("/")}/',
        ])
        return run_command(*args)
