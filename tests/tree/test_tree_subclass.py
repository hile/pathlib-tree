#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for pathlib_tree.tree.Tree subclases
"""
from pathlib_tree.tree import Tree, TreeItem


class FilePathItem(TreeItem):
    """
    Mock using separate child class for Tree directory loading
    """


class SubdirectoryPath(Tree):
    """
    Mock using separate child class for Tree directory loading
    """
    __file_loader_class__: Tree = FilePathItem


class TestTree(Tree):
    """
    Custom Tree object with separate models for directories and files loaders
    """
    __test__ = False
    __directory_loader_class__: TreeItem = SubdirectoryPath
    __file_loader_class__: Tree = FilePathItem


def test_tree_subclass_properties(parent_path):
    """
    Test subclassing Tree loads items with expected types
    """
    tree = TestTree(parent_path)
    assert len(list(iter(tree))) > 0
    for item in tree:
        if item.is_dir():
            assert isinstance(item, tree.__directory_loader_class__)
        if item.is_file():
            assert isinstance(item, tree.__file_loader_class__)
