"""
Unit tests for pathlib_tree.patterns path prefix matching
"""

from pathlib_tree.patterns import match_path_prefix


def test_match_path_prefix_full_path():
    """
    Test matching path prefixes returns True
    """
    assert match_path_prefix('/test', '/test/other directory/filename.txt')


def test_match_path_prefix_components():
    """
    Test matching path prefixes returns True
    """
    assert match_path_prefix(
        ['test'],
        ['test', 'other directory', 'filename.txt']
    )


def test_match_path_prefix_full_path_no_match():
    """
    Test matching different path prefixes returns False
    """
    assert not match_path_prefix('/test', '/testing/other directory/filename.txt')


def test_match_path_prefix_patterns():
    """
    Test matching different path prefixes returns False
    """
    assert match_path_prefix(
        '/test/*/filename.txt',
        '/test/other directory/filename.txt'
    )
    assert match_path_prefix(
        '/*/*/*.txt',
        '/test/other directory/filename.txt'
    )
    assert match_path_prefix(
        '/test/*',
        '/test/other directory/filename.txt'
    )


def test_match_path_prefix_patterns_no_match():
    """
    Test matching different path prefixes returns False
    """
    assert not match_path_prefix(
        '/test/mydata*/*.txt',
        '/test/other directory/filename.txt'
    )
    assert not match_path_prefix('/test/*', '/test')
