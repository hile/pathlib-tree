
import itertools
import pathlib
import os

from .errors import FilesystemError
from .patterns import match_path_patterns
from .utils import current_umask


class Tree(pathlib.Path):
    """
    Extend pathlib.Path to use for filesystem tree processing
    """
    # pylint: disable=protected-access
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    # pylint: disable=redefined-builtin
    # pylint: disable=unused-argument
    def __init__(self, path, create_missing=False, sorted=True, mode=None, excluded=None):
        self.excluded = excluded if excluded is not None else []
        self.sorted = sorted
        if create_missing and not self.exists():
            self.create(mode)

        self.__iter_items__ = None
        self.__iter_child__ = None
        self.__items__ = None
        self.__iterator__ = None

    def __repr__(self):
        return str(self)

    def create(self, mode=None):
        """
        Create directory

        Raises FilesystemError if path already exists or creation failed.
        """
        if self.exists():
            if self.is_dir():
                raise FilesystemError('Directory already exists: {}'.format(self))
            raise FilesystemError('File with path already exists: {}'.format(self))

        try:
            if mode is None:
                mode = '{:04o}'.format(current_umask() ^ int('777', 8))

            if isinstance(mode, str):
                mode = int(mode, 8)

            if not 0 <= mode <= 4095:
                raise ValueError('Invalid mode value')

        except ValueError as error:
            raise FilesystemError(
                'Error parsing filesystem mode value as octal {}: {}'.format(mode, error)
            )

        try:
            self.mkdir(mode)
        except OSError as error:
            raise FilesystemError(
                'Error creating directory {}: {}'.format(self, error)
            )

    def remove(self, recursive=False):
        """
        Remove tree
        """
        if not recursive and len(self) > 0:
            raise FileExistsError('Tree is not empty: {}'.format(self))
        for item in list(self):
            if not item.exists():
                continue
            if isinstance(item, Tree):
                item.remove(recursive)
            else:
                item.unlink()
        self.rmdir()

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
                if item.name in self.excluded:
                    continue
                if item.is_dir():
                    item = Tree(item, excluded=self.excluded)
                self.__iter_items__.append(item)
                self.__items__[str(item)] = item
            self.__iterator__ = itertools.chain(self.__iter_items__)

        try:
            if self.__iter_child__ is not None:
                try:
                    item = next(self.__iter_child__)
                    if str(item) not in self.__items__:
                        self.__items__[str(item)] = item
                    return item
                except StopIteration:
                    self.__iter_child__ = None

            item = next(self.__iterator__)
            if item.is_dir():
                self.__iter_child__ = Tree(item, sorted=self.sorted, excluded=self.excluded)
                self.__items__[str(self.__iter_child__)] = self.__iter_child__
            else:
                item = pathlib.Path(item)
            return item
        except StopIteration:
            self.__iterator__ = itertools.chain(self.__iter_items__)
            self.__iter_child__ = None
            raise StopIteration

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
