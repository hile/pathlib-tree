#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Filesystem file tree
"""
import filecmp
import hashlib
import itertools
import os
import pathlib

from datetime import datetime
from typing import Any, Iterator, List, Optional, Tuple, Union
from zoneinfo import ZoneInfo

from .exceptions import FilesystemError
from .patterns import match_path_patterns
from .utils import current_umask

#: Files and directories never included in tree scans
SKIPPED_PATHS = [
    '.DocumentRevisions-V100',
    '.Spotlight-V100',
    '.TemporaryItems',
    '.Trashes',
    '.fseventsd',
    '.metadata_never_index',
    'TheVolumeSettingsFolder',
]

#: Skipped hash algoritms (do not implement common call format)
SKIPPED_CHECKSUMS = (
    'shake_128',
    'shake_256',
)

# Default timezone for local filesystem timestamp parsing
DEFAULT_TIMEZONE = ZoneInfo('UTC')
#: Default checksum hash algorithm
DEFAULT_CHECKSUM = 'sha256'
#: Default block size when calculating file checksums
DEFAULT_CHECKSUM_BLOCK_SIZE = 2**20


class TreeItem(pathlib.Path):
    """
    File items in a tree

    Extends pathlib.Path with some properties and utility methods
    """
    # pylint: disable=protected-access
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    __checksums__ = {}

    @property
    def gid(self) -> int:
        """
        Return st_gid
        """
        return self.lstat().st_gid

    @property
    def uid(self) -> int:
        """
        Return st_uid
        """
        return self.lstat().st_uid

    @property
    def atime(self) -> datetime:
        """
        Return st_atime as UTC datetime
        """
        return datetime.fromtimestamp(self.lstat().st_atime).astimezone(DEFAULT_TIMEZONE)

    @property
    def ctime(self) -> datetime:
        """
        Return st_ctime as UTC datetime
        """
        return datetime.fromtimestamp(self.lstat().st_ctime).astimezone(DEFAULT_TIMEZONE)

    @property
    def mtime(self) -> datetime:
        """
        Return st_mtime as UTC datetime
        """
        return datetime.fromtimestamp(self.lstat().st_mtime).astimezone(DEFAULT_TIMEZONE)

    @property
    def size(self) -> int:
        """
        Return st_size
        """
        return self.lstat().st_size

    @property
    def magic(self) -> str:
        """
        Return file magic string
        """
        # pylint: disable=import-outside-toplevel
        try:
            from magic import Magic
        except ImportError as error:
            raise FilesystemError('Required libmagic library not available') from error
        try:
            with Magic() as handle:
                return handle.id_filename(str(self))
        except Exception as error:
            raise FilesystemError(f'Error reading file magic from {self}: {error}') from error

    def __get_cached_checksum__(self, algorithm: str) -> Optional[str]:
        """
        Get cached checksum if st_mtime is not changed
        """
        try:
            cached_item = self.__checksums__[algorithm]
            if cached_item['st_mtime'] != self.lstat().st_mtime:
                del self.__checksums__[algorithm]
                return None
            return cached_item['hex_digest']
        except KeyError:
            return None

    def checksum(self,
                 algorithm: str = DEFAULT_CHECKSUM,
                 block_size: int = DEFAULT_CHECKSUM_BLOCK_SIZE) -> str:
        """
        Calculate hex digest for file with specified checksum algorithm
        """
        if algorithm in SKIPPED_CHECKSUMS:
            raise FilesystemError(f'Calculating {algorithm} not supported')
        if not self.is_file() or not self.exists():
            raise FilesystemError(f'No such file: {self}')

        cached_checksum = self.__get_cached_checksum__(algorithm)
        if cached_checksum is not None:
            return cached_checksum
        try:
            hash_callback = getattr(hashlib, algorithm)()
        except AttributeError as error:
            raise FilesystemError(f'Unexpected algorithm: {algorithm}') from error

        with self.open('rb') as filedescriptor:
            while True:
                chunk = filedescriptor.read(block_size)
                if not chunk:
                    break
                hash_callback.update(chunk)

            hex_digest = hash_callback.hexdigest()
            self.__checksums__[algorithm] = {
                'st_mtime': self.lstat().st_mtime,
                'hex_digest': hex_digest
            }
            return hex_digest


class Tree(pathlib.Path):
    """
    Extend pathlib.Path to use for filesystem tree processing
    """
    create_missing: bool
    sorted: bool
    mode: str
    excluded: List[str]

    __directory_loader_class__: 'Tree' = None
    """Tree item loader for directories"""
    __file_loader_class__: TreeItem = None
    """Tree item loader class for files"""

    # pylint: disable=protected-access
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    # pylint: disable=redefined-builtin
    # pylint: disable=unused-argument
    def __init__(self,
                 path: Union[str, pathlib.Path],
                 create_missing: bool = False,
                 sorted: bool = True,
                 mode: str = None,
                 excluded: Optional[List[str]] = None):  # noqa
        self.excluded = self.__configure_excluded__(excluded)
        self.sorted = sorted  # noqa
        if create_missing and not self.exists():
            self.create(mode)

        self.__items__ = None
        self.__iter_items__ = None
        self.__iter_child__ = None
        self.__iterator__ = None
        self.reset()

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def __configure_excluded__(excluded: Optional[List[str]] = None) -> List[str]:
        """
        Merge excluded with skipped paths
        """
        if excluded is None:
            excluded = []
        for skipped in SKIPPED_PATHS:
            if skipped not in excluded:
                excluded.append(skipped)
        return excluded

    @property
    def __directory_loader__(self):
        """
        Get loader class for subdirectory items
        """
        if self.__directory_loader_class__ is not None:
            return self.__directory_loader_class__
        return self.__class__

    @property
    def __file_loader__(self):
        """
        Get loader class for file items
        """
        if self.__file_loader_class__ is not None:
            return self.__file_loader_class__
        return TreeItem

    def __getitem__(self, path: Union[str, pathlib.Path]) -> Any:
        """
        Get cached path item by path
        """
        if not self.__items__:
            list(self)
        if isinstance(path, pathlib.Path):
            path = str(path)

        return self.__items__[path]

    def __iter__(self) -> Iterator[Any]:
        return self

    def __load_tree__(self, item: Union[str, pathlib.Path]) -> TreeItem:
        """
        Load sub directory
        """
        # pylint: disable=not-callable
        return self.__directory_loader__(item, sorted=self.sorted, excluded=self.excluded)

    def __load_file__(self, item: Union[str, pathlib.Path]) -> TreeItem:
        """
        Load file item
        """
        # pylint: disable=not-callable
        return self.__file_loader__(item)

    # pylint: disable=too-many-branches
    def __next__(self):
        """
        Walk tree items recursively, returning Tree or Path objects

        Tree is walked depth first. If self.sorted is set, Tree items are sorted
        before iterating.
        """
        if not self.__items__:
            self.__iter_child__ = None
            self.__items__ = {}
            if self.sorted:
                try:
                    items = sorted(self.iterdir())
                except FileNotFoundError as error:
                    raise FilesystemError(f'{error}') from error
            else:
                items = self.iterdir()
            self.__iter_items__ = []
            try:
                for item in items:
                    if self.is_excluded(item):
                        continue
                    if item.is_dir():
                        item = self.__load_tree__(item)
                    else:
                        item = self.__load_file__(item)
                    self.__items__[str(item)] = item
                    self.__iter_items__.append(item)
            except FileNotFoundError as error:
                raise FilesystemError(f'{error}') from error
            self.__iterator__ = itertools.chain(self.__iter_items__)

        try:
            if self.__iter_child__ is not None:
                try:
                    item = next(self.__iter_child__)
                    if str(item) not in self.__items__:
                        if item.is_dir():
                            item = self.__load_tree__(item)
                        else:
                            item = self.__load_file__(item)
                        self.__items__[str(item)] = item
                    return item
                except StopIteration:
                    self.__iter_child__ = None

            item = next(self.__iterator__)
            if item.is_dir():
                item = self.__load_tree__(item)
                self.__iter_child__ = item
                self.__items__[str(self.__iter_child__)] = self.__iter_child__
            else:
                item = self.__load_file__(item)
            return item
        except StopIteration as stop:
            self.__iterator__ = itertools.chain(self.__iter_items__)
            self.__iter_child__ = None
            raise StopIteration from stop

    @property
    def is_empty(self) -> bool:
        """
        Check if tree is empty
        """
        return not list(self)

    def is_excluded(self, item: TreeItem) -> bool:
        """
        Check if item is excluded
        """
        if item.name in self.excluded:
            return True
        if match_path_patterns(self.excluded, self, item.name):
            return True
        return False

    def reset(self) -> None:
        """
        Result cached items loaded to the tree
        """
        self.__items__ = None
        self.__iter_items__ = None
        self.__iter_child__ = None
        self.__iterator__ = None

    def resolve(self, strict: bool = False) -> 'Tree':
        """
        Return correct type of tree from pathlib.Path.resolve() parent method
        """
        return self.__class__(path=super().resolve(strict), sorted=self.sorted, excluded=self.excluded)

    def create(self, mode: Optional[Union[int, str]] = None):
        """
        Create directory

        Raises FilesystemError if path already exists or creation failed.
        """
        if self.exists():
            if self.is_dir():
                raise FilesystemError(f'Directory already exists: {self}')
            raise FilesystemError(f'File with path already exists: {self}')

        try:
            if mode is None:
                value = current_umask() ^ int('777', 8)
                mode = f'{value:04o}'

            if isinstance(mode, str):
                mode = int(mode, 8)

            if not 0 <= mode <= 4095:
                raise ValueError('Invalid mode value')

        except ValueError as error:
            raise FilesystemError(f'Error parsing filesystem mode value as octal {mode}: {error}') from error

        try:
            self.mkdir(mode)
        except OSError as error:
            raise FilesystemError(f'Error creating directory {self}: {error}') from error

    def filter(self,
               patterns: Optional[List[str]] = None,
               extensions: Optional[List[str]] = None) -> 'TreeSearch':  # noqa
        """
        Filter specified name patterns from tree

        Patterns can be either a glob pattern or list of glob patterns
        """
        return TreeSearch(self, list(self)).filter(patterns, extensions)

    def exclude(self, patterns: Optional[List[str]] = None) -> 'TreeSearch':
        """
        Exclude specified name patterns from tree

        Patterns can be either a glob pattern or list of glob patterns
        """
        return TreeSearch(self, list(self)).exclude(patterns)

    def remove(self, recursive: bool = False) -> None:
        """
        Remove tree from filesystem
        """
        if not recursive and not self.is_empty:
            raise FilesystemError(f'Tree is not empty: {self}')

        for item in list(self):
            if not item.exists():
                continue
            if isinstance(item, self.__directory_loader__):
                item.remove(recursive)
            else:
                item.unlink()
        self.rmdir()

    def diff(self, other: Union[str, 'Tree']) -> Tuple[List[TreeItem], List[TreeItem], List[TreeItem]]:
        """
        Run simple diff using filecmp.cmp against files in other tree, returning differences in files
        and files missing from either directory

        Returns three lists with:
        - list of files with differing contents
        - files missing from this tree
        - files missing from other tree
        """
        if not isinstance(other, Tree):
            other = Tree(str(other), sorted=self.sorted, excluded=self.excluded)

        missing_self = []
        missing_other = []
        different = []
        for item in self:
            path = other.joinpath(item.relative_to(self))
            if item.is_dir() or path.is_dir():
                if item.is_dir() and path.is_file():
                    missing_self.append(path)
                if item.is_file() and path.is_dir():
                    missing_other.append(path)
            elif path.exists():
                if not filecmp.cmp(str(item), str(path), shallow=False):
                    different.append(path)
            else:
                missing_other.append(path)

        for item in other:
            path = self.joinpath(item.relative_to(other))
            if item.is_dir() or path.is_dir():
                if item.is_dir() and path.is_file():
                    missing_other.append(path)
                if item.is_file() and path.is_dir():
                    missing_self.append(path)
            elif not path.exists():
                missing_self.append(path)

        return different, missing_self, missing_other


class TreeSearch(list):
    """
    Chainable tree search results
    """
    tree: Tree

    def __init__(self, tree: Tree, items: List[TreeItem]) -> None:
        self.tree = tree
        super().__init__(items)

    def filter(self,
               patterns: Union[str, List[str]] = None,
               extensions: Optional[List[str]] = None) -> 'TreeSearch':  # noqa
        """
        Match specified patterns from matched items
        """
        if isinstance(extensions, str):
            extensions = extensions.split(',')
        if isinstance(patterns, str):
            patterns = [patterns]

        matches = []
        for item in self:
            if extensions and item.suffix in extensions:
                matches.append(item)
            if patterns and match_path_patterns(patterns, self.tree, item):
                matches.append(item)
        return self.__class__(self.tree, matches)

    def exclude(self, patterns: Union[str, List[str]] = None) -> 'TreeSearch':
        """
        Exclude specified patterns from matched items
        """
        if isinstance(patterns, str):
            patterns = [patterns]

        matches = []
        for item in self:
            if not match_path_patterns(patterns, self.tree, item):
                matches.append(item)
        return self.__class__(self.tree, matches)
