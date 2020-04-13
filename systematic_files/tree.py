"""
Filesystem file tree
"""

import hashlib
import itertools
import pathlib
import os

from datetime import datetime

import pytz

from .errors import FilesystemError
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
    def gid(self):
        """
        Return st_gid
        """
        return self.lstat().st_gid

    @property
    def uid(self):
        """
        Return st_uid
        """
        return self.lstat().st_uid

    @property
    def atime(self):
        """
        Return st_atime as UTC datetime
        """
        return datetime.fromtimestamp(self.lstat().st_atime).astimezone(pytz.UTC)

    @property
    def ctime(self):
        """
        Return st_ctime as UTC datetime
        """
        return datetime.fromtimestamp(self.lstat().st_ctime).astimezone(pytz.UTC)

    @property
    def mtime(self):
        """
        Return st_mtime as UTC datetime
        """
        return datetime.fromtimestamp(self.lstat().st_mtime).astimezone(pytz.UTC)

    @property
    def size(self):
        """
        Return st_size
        """
        return self.lstat().st_size

    def __get_cached_checksum__(self, algorithm):
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

    def checksum(self, algorithm=DEFAULT_CHECKSUM, block_size=DEFAULT_CHECKSUM_BLOCK_SIZE):
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
        except AttributeError:
            raise FilesystemError(f'Unexpected algorithm: {algorithm}')

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
    file_class = TreeItem
    '''Tree item loader class for files'''

    # pylint: disable=protected-access
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    # pylint: disable=redefined-builtin
    # pylint: disable=unused-argument
    def __init__(self, path, create_missing=False, sorted=True, mode=None, excluded=None):
        self.excluded = excluded if excluded is not None else []
        self.excluded.extend(SKIPPED_PATHS)
        self.sorted = sorted
        if create_missing and not self.exists():
            self.create(mode)

        self.__iter_items__ = None
        self.__iter_child__ = None
        self.__items__ = None
        self.__iterator__ = None

    def __repr__(self):
        return str(self)

    def __getitem__(self, path):
        """
        Get cached path item by path
        """
        if not self.__items__:
            list(self)
        if isinstance(path, pathlib.Path):
            path = str(path)

        return self.__items__[path]

    def __iter__(self):
        return self

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
                items = sorted(self.iterdir())
            else:
                items = self.iterdir()
            self.__iter_items__ = []
            for item in items:
                if item.name in self.excluded or match_path_patterns(self.excluded, self, item.name):
                    continue
                if item.is_dir():
                    item = Tree(item, excluded=self.excluded)
                self.__iter_items__.append(item)
                self.__items__[str(item)] = self.file_class(item)
            self.__iterator__ = itertools.chain(self.__iter_items__)

        try:
            if self.__iter_child__ is not None:
                try:
                    item = next(self.__iter_child__)
                    if str(item) not in self.__items__:
                        self.__items__[str(item)] = self.file_class(item)
                    return item
                except StopIteration:
                    self.__iter_child__ = None

            item = next(self.__iterator__)
            if item.is_dir():
                item = Tree(item, sorted=self.sorted, excluded=self.excluded)
                self.__iter_child__ = item
                self.__items__[str(self.__iter_child__)] = self.__iter_child__
            else:
                item = self.file_class(item)
            return item
        except StopIteration:
            self.__iterator__ = itertools.chain(self.__iter_items__)
            self.__iter_child__ = None
            raise StopIteration

    @property
    def is_empty(self):
        """
        Check if tree is empty
        """
        return list(self) == []

    def create(self, mode=None):
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
            raise FilesystemError(f'Error parsing filesystem mode value as octal {mode}: {error}')

        try:
            self.mkdir(mode)
        except OSError as error:
            raise FilesystemError(f'Error creating directory {self}: {error}')

    def filter(self, patterns):
        """
        Filter specified name patterns from tree

        Patterns can be either a glob pattern or list of glob patterns
        """
        return TreeSearch(self, list(self)).filter(patterns)

    def exclude(self, patterns):
        """
        Exclude specified name patterns from tree

        Patterns can be either a glob pattern or list of glob patterns
        """
        return TreeSearch(self, list(self)).exclude(patterns)

    def remove(self, recursive=False):
        """
        Remove tree
        """
        if not recursive and not self.is_empty:
            raise FilesystemError(f'Tree is not empty: {self}')

        for item in list(self):
            if not item.exists():
                continue
            if isinstance(item, Tree):
                item.remove(recursive)
            else:
                item.unlink()
        self.rmdir()


class TreeSearch(list):
    """
    Chainable tree search results
    """
    def __init__(self, tree, items):
        self.tree = tree
        super().__init__(items)

    def filter(self, patterns):
        """
        Match specified patterns from matched items
        """
        if isinstance(patterns, str):
            patterns = [patterns]

        matches = []
        for item in self:
            if match_path_patterns(patterns, self.tree, item):
                matches.append(item)
        return TreeSearch(self.tree, matches)

    def exclude(self, patterns):
        """
        Exclude specified patterns from matched items
        """
        if isinstance(patterns, str):
            patterns = [patterns]

        matches = []
        for item in self:
            if not match_path_patterns(patterns, self.tree, item):
                matches.append(item)
        return TreeSearch(self.tree, matches)
