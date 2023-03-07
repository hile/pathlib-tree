#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for pathlib_tree.tree.Tree tree diff() method
"""
from pathlib import Path

from pathlib_tree import Tree

from .conftest import (
    MOCK_TREE_DIFFERENT_COUNT,
    MOCK_TREE_A_MISSING_COUNT,
    MOCK_TREE_B_MISSING_COUNT,
)


def test_tree_diff_same_tree(parent_path):
    """
    Test diff of two identical Tree objects
    """
    different, missing_self, missing_other = Tree(
        parent_path
    ).diff(Tree(parent_path))
    assert different == []
    assert missing_self == []
    assert missing_other == []


def test_tree_diff_same_str_other(parent_path):
    """
    Test diff of two identical Tree objects
    """
    different, missing_self, missing_other = Tree(
        parent_path
    ).diff(str(Path(parent_path).resolve()))
    assert different == []
    assert missing_self == []
    assert missing_other == []


def test_tree_diff_same_path_other(parent_path):
    """
    Test diff of two identical Tree objects
    """
    different, missing_self, missing_other = Tree(
        parent_path
    ).diff(Path(parent_path).resolve())
    assert different == []
    assert missing_self == []
    assert missing_other == []


def test_tree_diff_other_tree(parent_path, tests_path):
    """
    Test diff of two different Tree objects
    """
    different, missing_self, missing_other = Tree(
        parent_path
    ).diff(tests_path)
    assert different != []
    assert missing_self != []
    assert missing_other != []


def test_tree_diff_mock_trees(mock_tree_a, mock_tree_b):
    """
    Test diff of crafted test trees in the tests/mock directory. Check the diff
    files count matches expected counters
    """
    different, missing_a, missing_b = mock_tree_a.diff(mock_tree_b)
    assert len(different) == MOCK_TREE_DIFFERENT_COUNT
    assert len(missing_a) == MOCK_TREE_A_MISSING_COUNT
    assert len(missing_b) == MOCK_TREE_B_MISSING_COUNT
