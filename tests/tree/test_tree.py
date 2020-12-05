"""
Unit tests for pathlib_tree.tree.Tree class
"""

import hashlib
import pathlib
import shutil
import stat

from datetime import datetime

import pytest

from pathlib_tree.tree import Tree, TreeItem, FilesystemError, SKIPPED_CHECKSUMS


def validate_tree(path, tree):
    """
    Validate loaded tree item for valid directory
    """
    assert tree.__repr__() == path
    assert tree.exists()
    assert tree.is_dir()
    return tree


def validate_tree_iterator_item(tree, item):
    """
    Validate item from tree iterator
    """
    assert isinstance(item, (Tree, pathlib.Path))
    if item.is_dir():
        assert isinstance(item, tree.__directory_loader__)
    else:
        assert isinstance(item, tree.__file_loader__)
    assert tree[item] == item


def test_tree_current_directory():
    """
    Test loading this directory as tree
    """
    work_directory = str(pathlib.Path(__file__).parent)
    validate_tree(work_directory, Tree(work_directory))


def test_tree_current_directory_create_missing_flag_true():
    """
    Test loading this directory as tree with create_missing = True
    """
    work_directory = str(pathlib.Path(__file__).parent)
    validate_tree(work_directory, Tree(work_directory, create_missing=True))


def test_tree_current_directory_missing_path():
    """
    Test loading this directory as tree and looking up unknown filename
    """
    work_directory = str(pathlib.Path(__file__).parent)
    tree = Tree(work_directory)
    validate_tree(work_directory, tree)
    with pytest.raises(KeyError):
        assert tree['8E8A747A-0285-4D5B-B59C-A0300B1607E3'] is None


def test_tree_current_directory_file_attributes():
    """
    Test loading this directory as tree and looking up current file and
    custom attributes for TreeItem class
    """
    work_directory = str(pathlib.Path(__file__).parent)
    tree = Tree(work_directory)
    print(tree)
    item = tree[str(pathlib.Path(__file__))]
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


def test_tree_item_checksum_missing_file(tmpdir):
    """
    Test calculating checksum for missing file
    """
    item = TreeItem(pathlib.Path(tmpdir, 'missing-file'))
    with pytest.raises(FilesystemError):
        item.checksum()


def test_tree_invalid_path():
    """
    Test loading invalid path as tree
    """
    tree = Tree('8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    assert not tree.exists()


def test_tree_iterating_test_directory():
    """
    Test iterating over this test data directory
    """
    tree = Tree(pathlib.Path(__file__).parent)
    assert tree.exists()
    assert tree.sorted  # pylint: disable=W0613, W0622

    previous = None
    for item in tree:
        validate_tree_iterator_item(tree, item)
        if previous is not None:
            assert previous < item
        previous = item


def test_tree_skipped_filenames(tmpdir):
    """
    Test tree with skipped filenames
    """
    tree = Tree(tmpdir)

    filename = '.metadata_never_index'
    skipped_file = pathlib.Path(tree, filename)
    skipped_file.touch()
    assert skipped_file.is_file()

    tree = Tree(tmpdir)
    with pytest.raises(StopIteration):
        next(tree)
    assert skipped_file not in tree


def test_tree_skipped_dirnames(tmpdir):
    """
    Test tree with skipped directory name patterns
    """
    tree = Tree(tmpdir)

    skipped_file = pathlib.Path(tree, 'skipped/test.yml')
    skipped_file.parent.mkdir()
    skipped_file.touch()
    assert skipped_file.is_file()

    tree = Tree(tmpdir, excluded=['skipped/'])
    with pytest.raises(StopIteration):
        next(tree)
    assert skipped_file not in tree


def test_tree_iterating_test_directory_sorted():
    """
    Test iterating over this test data directory as unsorted items
    """
    tree = Tree(pathlib.Path(__file__).parent, sorted=False)
    assert tree.exists()
    assert not tree.sorted  # pylint: disable=W0613, W0622

    for item in tree:
        validate_tree_iterator_item(tree, item)
    total_items = len(tree.__items__)
    # Iterate tree again to trigger cached iteration
    for item in tree:
        validate_tree_iterator_item(tree, item)
    assert len(tree.__items__) == total_items


def test_tree_existing_file_create():
    """
    Test loading existing file path as tree and creating iit
    """
    tree = Tree(__file__)
    assert tree.exists()
    with pytest.raises(FilesystemError):
        tree.create()


def test_tree_invalid_path_create(tmpdir):
    """
    Test loading temporary path as tree and creating directory manually
    """
    path = pathlib.Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create()
    assert tree.exists()
    with pytest.raises(StopIteration):
        next(tree)
    with pytest.raises(FilesystemError):
        tree.create()


def test_tree_invalid_path_create_missing(tmpdir):
    """
    Test loading temporary path as tree and creating directory manually
    with specified invalid mode
    """
    path = pathlib.Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path, create_missing=True)
    assert tree.exists()


def test_tree_invalid_path_create_with_invalid_modes(tmpdir):
    """
    Test loading temporary path as tree and creating directory manually
    with specified invalid mode
    """
    path = pathlib.Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()

    for mode in ('', '11700', -1, 12345678):
        with pytest.raises(FilesystemError):
            tree.create(mode)


def test_tree_invalid_path_create_with_mode(tmpdir):
    """
    Test loading temporary path as tree and creating directory manually
    with specified mode
    """
    mode = '2700'
    path = pathlib.Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create(mode)
    assert tree.exists()
    assert stat.S_IMODE(tree.stat().st_mode) == int('0700', 8)
    tree.rmdir()


def test_tree_invalid_path_create_with_mode_as_int(tmpdir):
    """
    Test loading temporary path as tree and creating directory manually
    with specified mode
    """
    mode = int('2700', 8)
    path = pathlib.Path(tmpdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create(mode)
    assert tree.exists()
    assert stat.S_IMODE(tree.stat().st_mode) == int('0700', 8)
    tree.rmdir()


# pylint: disable=unused-argument
def test_tree_create_permission_denied(mock_path_not_exists, mock_path_mkdir_permission_denied):
    """
    Test creating directory without permissions for path
    """
    tree = Tree('/8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    assert not tree.exists()
    with pytest.raises(FilesystemError):
        tree.create()


def test_tree_create_and_remove(tmpdir):
    """
    Test creating directory without permissions for path
    """
    parent = pathlib.Path(__file__).parent
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
