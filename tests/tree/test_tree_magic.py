#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for pathlib_tree.tree.Tree file magic handling
"""
import pytest

from pathlib_tree.exceptions import FilesystemError
from pathlib_tree.tree import Tree, TreeItem


# pylint: disable=unused-argument
def test_tree_magic_import_error(parent_path, libmagic_import_error) -> None:
    """
    Test tree magic when magic library is not deteted as installed
    """
    tree = Tree(parent_path)
    assert len(list(iter(tree))) > 0
    for item in tree:
        if isinstance(item, TreeItem):
            with pytest.raises(FilesystemError):
                item.magic  # pylint: disable=pointless-statement


# pylint: disable=unused-argument
def test_tree_magic_call_error(parent_path, libmagic_call_error) -> None:
    """
    Test tree magic when magic library raises an exception
    """
    tree = Tree(parent_path)
    assert len(list(iter(tree))) > 0
    for item in tree:
        if isinstance(item, TreeItem):
            with pytest.raises(FilesystemError):
                item.magic  # pylint: disable=pointless-statement


def test_tree_magic(parent_path) -> None:
    """
    Test tree magic when magic library is installed as expected
    """
    tree = Tree(parent_path)
    assert len(list(iter(tree))) > 0
    for item in tree:
        if isinstance(item, TreeItem):
            assert isinstance(item.magic, str)
