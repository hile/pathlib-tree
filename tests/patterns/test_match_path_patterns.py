"""
Unit tests for pathlib_tree.patterns functions
"""

from pathlib_tree.patterns import match_path_patterns


def test_match_simple_patterns_no_match():
    """
    Test simple relative tree pattern match case
    """
    patterns = (
        '*/*.txt',
    )
    assert not match_path_patterns(
        patterns,
        '/data',
        '/test/other files/filename.txt'
    )


def test_match_simple_patterns_direct_match():
    """
    Test simple relative tree pattern match case
    """
    patterns = (
        'filename.txt',
        '*/*.txt',
    )
    assert match_path_patterns(
        patterns,
        '/test',
        '/test/other files/filename.txt'
    )
    patterns = (
        'test/other files/'
    )
    assert match_path_patterns(
        patterns,
        '/test/other files',
        '/test/other files/filename.txt'
    )


def test_match_simple_patterns():
    """
    Test simple relative tree pattern match case
    """
    patterns = (
        'filename.wav',
        '*/*.txt',
    )
    assert match_path_patterns(
        patterns,
        '/test',
        '/test/other files/filename.txt'
    )


def test_match_prefix_match():
    """
    Test simple relative tree pattern match case
    """
    patterns = (
        'other files/*.txt',
    )
    assert match_path_patterns(
        patterns,
        '/test',
        '/test/other files/filename.txt'
    )


def test_match_prefix_glob_match():
    """
    Test simple relative tree pattern match case
    """
    patterns = (
        '*/other files/*',
    )
    assert match_path_patterns(
        patterns,
        '/test',
        '/test/data/other files/deeper/filename.txt'
    )


def test_match_relative_pattern():
    """
    Test matching a relative path pattern
    """
    patterns = (
        'other */*.wav',
        '*/*.txt',
    )
    assert match_path_patterns(
        patterns,
        '/test/data',
        '/test/data/other files/filename.txt'
    )
