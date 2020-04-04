
import os
import pathlib
import stat
import tempfile

import pytest

from systematic_files.tree import Tree, FilesystemError


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
        assert isinstance(item, Tree)
    else:
        assert isinstance(item, pathlib.Path)

    assert tree[item] == item


def test_tree_current_directory():
    """
    Test loading current directory as tree
    """
    work_directory = os.getcwd()
    validate_tree(work_directory, Tree(work_directory))


def test_tree_current_directory_create_missing_flag_true():
    """
    Test loading current directory as tree with create_missing = True
    """
    work_directory = os.getcwd()
    validate_tree(work_directory, Tree(work_directory, create_missing=True))


def test_tree_current_directory_missing_path():
    """
    Test loading current directory as tree
    """
    work_directory = os.getcwd()
    tree = Tree(work_directory)
    validate_tree(work_directory, tree)
    with pytest.raises(KeyError):
        assert tree['8E8A747A-0285-4D5B-B59C-A0300B1607E3'] is None


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


def test_tree_invalid_path_create():
    """
    Test loading temporary path as tree and creating directory manually
    """
    tempdir = tempfile.mkdtemp()
    path = pathlib.Path(tempdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create()
    assert tree.exists()
    with pytest.raises(StopIteration):
        next(tree)
    with pytest.raises(FilesystemError):
        tree.create()


def test_tree_invalid_path_create_missing():
    """
    Test loading temporary path as tree and creating directory manually
    with specified invalid mode
    """
    tempdir = tempfile.mkdtemp()
    path = pathlib.Path(tempdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path, create_missing=True)
    assert tree.exists()


def test_tree_invalid_path_create_with_invalid_modes():
    """
    Test loading temporary path as tree and creating directory manually
    with specified invalid mode
    """
    tempdir = tempfile.mkdtemp()
    path = pathlib.Path(tempdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()

    for mode in ('', '11700', -1, 12345678):
        with pytest.raises(FilesystemError):
            tree.create(mode)


def test_tree_invalid_path_create_with_mode():
    """
    Test loading temporary path as tree and creating directory manually
    with specified mode
    """
    tempdir = tempfile.mkdtemp()
    mode = '2700'
    path = pathlib.Path(tempdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create(mode)
    assert tree.exists()
    assert stat.S_IMODE(tree.stat().st_mode) == int('0700', 8)
    tree.rmdir()


def test_tree_invalid_path_create_with_mode_as_int():
    """
    Test loading temporary path as tree and creating directory manually
    with specified mode
    """
    tempdir = tempfile.mkdtemp()
    mode = int('2700', 8)
    path = pathlib.Path(tempdir, '8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    tree = Tree(path)
    assert not tree.exists()
    tree.create(mode)
    assert tree.exists()
    assert stat.S_IMODE(tree.stat().st_mode) == int('0700', 8)
    tree.rmdir()


def test_tree_create_permission_denied():
    """
    Test creating directory without permissions for path
    """
    tree = Tree('/8E8A747A-0285-4D5B-B59C-A0300B1607E3')
    assert not tree.exists()
    with pytest.raises(FilesystemError):
        tree.create()
