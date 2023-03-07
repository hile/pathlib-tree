#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for pathlib_tree.tree.Tree searches
"""
from pathlib import Path

from pathlib_tree.tree import Tree

MOCK_TEXT_FILE_COUNT = 3


def test_tree_search_filter(mock_test_tree) -> None:
    """
    Test simple filtering files from tree
    """
    tree = Tree(mock_test_tree)
    assert len(tree.filter('foo')) == 4
    assert len(tree.filter('foo/*')) == 3
    assert len(tree.filter(['a', 'b'])) == 2
    assert len(tree.filter(['a*', '*.tst'])) == 4
    assert len(tree.filter('*.txt')) == MOCK_TEXT_FILE_COUNT
    for item in tree.filter('*.txt'):
        assert isinstance(item, (Tree, Path))


def test_tree_search_exclude(mock_test_tree) -> None:
    """
    Test simple filtering files from tree
    """
    tree = Tree(mock_test_tree)
    assert len(tree.exclude('foo')) == 8
    assert len(tree.exclude('foo/*')) == 9
    assert len(tree.exclude(['a', 'b'])) == 10
    for item in tree.exclude(['a', 'b']):
        assert isinstance(item, (Tree, Path))


def test_tree_search_filter_extensions_str(mock_test_tree) -> None:
    """
    Test filtering search tree by file extensions
    """
    tree = Tree(mock_test_tree)
    assert len(tree.filter(extensions='.txt')) == MOCK_TEXT_FILE_COUNT


def test_tree_search_filter_extensions_list(mock_test_tree) -> None:
    """
    Test filtering search tree by file extensions
    """
    tree = Tree(mock_test_tree)
    assert len(tree.filter(extensions=['.txt', '.md'])) == MOCK_TEXT_FILE_COUNT


def test_tree_search_chaining(mock_test_tree) -> None:
    """
    Test chaining of filtering files from tree
    """
    tree = Tree(mock_test_tree)
    assert len(tree.exclude('foo').filter('a*')) == 1
    assert len(tree.filter('a*').exclude('foo')) == 1
