#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for pathlib_tree.tree.Tree class
"""
import hashlib
import shutil
import stat

from datetime import datetime
from pathlib import Path
import pytest

from pathlib_tree import Tree as MainLevelTree
from pathlib_tree.tree import Tree, TreeItem, SKIPPED_CHECKSUMS
from pathlib_tree.exceptions import FilesystemError


def validate_tree(path, tree) -> None:
    """
    Validate loaded tree item for valid directory
    """
    assert tree.__repr__() == path
    assert tree.exists()
    assert tree.is_dir()
    return tree


def validate_tree_iterator_item(tree, item) -> None:
    """
    Validate item from tree iterator
    """
    assert isinstance(item, (Tree, Path))
    if item.is_dir():
        assert isinstance(item, tree.__directory_loader__)
    else:
        assert isinstance(item, tree.__file_loader__)
    assert tree[item] == item


def test_tree_main_import(parent_path) -> None:
    """
    Ensure the tree object imported from top level is Tree object
    """
    obj = MainLevelTree(parent_path)
    assert isinstance(obj, Tree)


def test_tree_current_directory(parent_path) -> None:
    """
    Test loading this directory as tree
    """
    validate_tree(parent_path, Tree(parent_path))


def test_tree_missing_directory_iterator(tmpdir) -> None:
    """
    Test iterating Tree a path that does not exist
    """
    with pytest.raises(FilesystemError):
        next(Tree(str(Path(tmpdir.strpath, 'missing-directory')), sorted=False))


def test_tree_missing_directory_sorted_iterator(tmpdir) -> None:
    """
    Test iterating sorted Tree for a path that does not exist
    """
    with pytest.raises(FilesystemError):
        next(Tree(str(Path(tmpdir.strpath, 'missing-directory')), sorted=True))


def test_tree_current_directory_create_missing_flag_true(parent_path) -> None:
    """
    Test loading this directory as tree with create_missing = True
    """
    validate_tree(parent_path, Tree(parent_path, create_missing=True))


def test_tree_current_directory_missing_path(parent_path) -> None:
    """
    Test loading this directory as tree and looking up unknown filename
    """
    tree = Tree(parent_path)
    validate_tree(parent_path, tree)
    with pytest.raises(KeyError):
        assert tree['8E8A747A-0285-4D5B-B59C-A0300B1607E3'] is None


def test_tree_current_directory_file_attributes(parent_path) -> None:
    """
    Test loading this directory as tree and looking up current file and
    custom attributes for TreeItem class
    """
    tree = Tree(parent_path)
    item = tree[str(Path(__file__))]
    assert isinstance(item, tree.__file_loader__)

    for attr in ('uid', 'gid', 'size'):
        value = getattr(item, attr)
        assert isinstance(value, int)

    for attr in ('atime', 'ctime', 'mtime'):
        value = getattr(item, attr)
        assert isinstance(value, datetime)

    with pytest.raises(FilesystemError):
        item.checksum('rot13')

    for hash_algorithm in hashlib.algorithms_guaranteed:
        if hash_algorithm in SKIPPED_CHECKSUMS:
            continue
        checksum = item.checksum(hash_algorithm)
        assert isinstance(checksum, str)
        assert hash_algorithm in item.__checksums__

    for hash_algorithm in hashlib.algorithms_guaranteed:
        if hash_algorithm in SKIPPED_CHECKSUMS:
            continue
        checksum = item.checksum(hash_algorithm)
        assert isinstance(checksum, str)

    item.touch()
    item.checksum()

    for hash_algorithm in SKIPPED_CHECKSUMS:
        with pytest.raises(FilesystemError):
            item.checksum(hash_algorithm)


def test_tree_resolve(tmpdir) -> None:
    """
    Test Tree resolve() method returns correct type
    """
    exclude_list = ['a', 'b', 'c']
    tree = Tree(tmpdir.strpath, excluded=exclude_list)
    resolved = tree.resolve()
    assert isinstance(resolved, Tree)
    assert resolved.excluded == exclude_list


def test_tree_item_checksum_missing_file(tmpdir) -> None:
    """
    Test calculating checksum for missing file
    """
    item = TreeItem(Path(tmpdir, 'missing-file'))
    with pytest.raises(FilesystemError):
        item.checksum()


def test_tree_invalid_path() -> None:
    """
    Test loading invalid path as tree
    """
    tree = Tree('8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    assert not tree.exists()


def test_tree_iterating_test_directory(parent_path) -> None:
    """
    Test iterating over this test data directory
    """
    tree = Tree(parent_path)
    assert tree.exists()
    assert tree.sorted  # pylint: disable=W0613, W0622

    previous = None
    for item in tree:
        validate_tree_iterator_item(tree, item)
        if previous is not None:
            assert previous < item
        previous = item


def test_tree_skipped_filenames(tmpdir) -> None:
    """
    Test tree with skipped filenames
    """
    tree = Tree(tmpdir)

    filename = '.metadata_never_index'
    skipped_file = Path(tree, filename)
    skipped_file.touch()
    assert skipped_file.is_file()

    tree = Tree(tmpdir)
    with pytest.raises(StopIteration):
        next(tree)
    assert skipped_file not in tree


def test_tree_skipped_dirnames(tmpdir) -> None:
    """
    Test tree with skipped directory name patterns
    """
    tree = Tree(tmpdir)

    skipped_file = Path(tree, 'skipped/test.yml')
    skipped_file.parent.mkdir()
    skipped_file.touch()
    assert skipped_file.is_file()

    tree = Tree(tmpdir, excluded=['skipped/'])
    with pytest.raises(StopIteration):
        next(tree)
    assert skipped_file not in tree


def test_tree_iterating_test_directory_sorted(parent_path) -> None:
    """
    Test iterating over this test data directory as unsorted items
    """
    tree = Tree(parent_path, sorted=False)
    assert tree.exists()
    assert not tree.sorted  # pylint: disable=W0613, W0622

    for item in tree:
        validate_tree_iterator_item(tree, item)
    total_items = len(tree.__items__)
    # Iterate tree again to trigger cached iteration
    for item in tree:
        validate_tree_iterator_item(tree, item)
    assert len(tree.__items__) == total_items


def test_tree_existing_file_create() -> None:
    """
    Test loading existing file path as tree and creating iit
    """
    tree = Tree(__file__)
    assert tree.exists()
    with pytest.raises(FilesystemError):
        tree.create()


def test_tree_invalid_path_create(tmpdir) -> None:
    """
    Test loading temporary path as tree and creating directory manually
    """
    path = Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create()
    assert tree.exists()
    with pytest.raises(StopIteration):
        next(tree)
    with pytest.raises(FilesystemError):
        tree.create()


def test_tree_invalid_path_create_missing(tmpdir) -> None:
    """
    Test loading temporary path as tree and creating directory manually
    with specified invalid mode
    """
    path = Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path, create_missing=True)
    assert tree.exists()


def test_tree_invalid_path_create_with_invalid_modes(tmpdir) -> None:
    """
    Test loading temporary path as tree and creating directory manually
    with specified invalid mode
    """
    path = Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()

    for mode in ('', '11700', -1, 12345678):
        with pytest.raises(FilesystemError):
            tree.create(mode)


def test_tree_invalid_path_create_with_mode(tmpdir) -> None:
    """
    Test loading temporary path as tree and creating directory manually
    with specified mode
    """
    mode = '2700'
    path = Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create(mode)
    assert tree.exists()
    assert stat.S_IMODE(tree.stat().st_mode) == int('0700', 8)
    tree.rmdir()


def test_tree_invalid_path_create_with_mode_as_int(tmpdir) -> None:
    """
    Test loading temporary path as tree and creating directory manually
    with specified mode
    """
    mode = int('2700', 8)
    path = Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create(mode)
    assert tree.exists()
    assert stat.S_IMODE(tree.stat().st_mode) == int('0700', 8)
    tree.rmdir()


# pylint: disable=unused-argument
def test_tree_create_permission_denied(
        mock_path_not_exists,
        mock_path_mkdir_permission_denied) -> None:
    """
    Test creating directory without permissions for path
    """
    tree = Tree('/8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    assert not tree.exists()
    with pytest.raises(FilesystemError):
        tree.create()


def test_tree_create_and_remove(tmpdir) -> None:
    """
    Test creating directory without permissions for path
    """
    parent = Path(__file__).parent
    tree = Tree(tmpdir, 'test-target')
    assert tree.exists()
    assert tree.is_empty is True

    tree.remove()
    tree.create()

    shutil.copytree(parent, tree.joinpath('data'))
    with pytest.raises(FilesystemError):
        tree.remove()

    tree.remove(recursive=True)
    assert not tree.exists()
