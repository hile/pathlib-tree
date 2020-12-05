"""
Unit tests for pathlib_tree.tree.Tree searches
"""

import os

from pathlib import Path

from pathlib_tree.tree import Tree

TEST_DIRECTORY_DATA = [
    {
        'name': 'foo',
        'children': [
            'a',
            'b',
            'c'
        ],
    },
    {
        'name': 'bar',
        'children': [
            'aa.tst',
            'bb.tst',
            'cc.tst',
            {
                'name': 'baz',
                'children': [
                    'd.txt',
                    'dd.txt',
                    'ddd.txt',
                ]
            }
        ]
    }
]


def create_test_directory(tmpdir):
    """
    Create test directory for filtering searches
    """
    def create_directory_items(prefix, item):
        path = os.path.join(prefix, item['name'])
        os.makedirs(path)
        for child in item.get('children', []):
            if isinstance(child, dict):
                create_directory_items(path, child)
            else:
                filename = os.path.join(path, child)
                with open(filename, 'w') as filedescriptor:
                    filedescriptor.write('\n')

    for item in TEST_DIRECTORY_DATA:
        create_directory_items(tmpdir, item)
    return tmpdir


def test_tree_search_filter(tmpdir):
    """
    Test simple filtering files from tree
    """
    path = create_test_directory(tmpdir)
    tree = Tree(path)
    assert tree.exists()

    assert len(tree.filter('foo')) == 4
    assert len(tree.filter('foo/*')) == 3
    assert len(tree.filter(['a', 'b'])) == 2
    assert len(tree.filter(['a*', '*.tst'])) == 4
    assert len(tree.filter('*.txt')) == 3
    for item in tree.filter('*.txt'):
        assert isinstance(item, (Tree, Path))


def test_tree_search_exclude(tmpdir):
    """
    Test simple filtering files from tree
    """
    path = create_test_directory(tmpdir)
    tree = Tree(path)
    assert tree.exists()

    assert len(tree.exclude('foo')) == 8
    assert len(tree.exclude('foo/*')) == 9
    assert len(tree.exclude(['a', 'b'])) == 10
    for item in tree.exclude(['a', 'b']):
        assert isinstance(item, (Tree, Path))


def test_tree_search_chaining(tmpdir):
    """
    Test chaininng of filtering files from tree
    """
    path = create_test_directory(tmpdir)
    tree = Tree(path)
    assert tree.exists()

    assert len(tree.exclude('foo').filter('a*')) == 1
    assert len(tree.filter('a*').exclude('foo')) == 1
