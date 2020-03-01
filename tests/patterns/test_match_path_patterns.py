
import unittest

from systematic_files.patterns import match_path_patterns


class TestMatchPathPatterns(unittest.TestCase):
    """
    Test the patch patterns match utility pattern method
    """

    def test_match_simple_patterns_no_match(self):
        """
        Test simple relative tree pattern match case
        """
        patterns = (
            '*/*.txt',
        )
        self.assertFalse(match_path_patterns(
            patterns,
            '/data',
            '/test/other files/filename.txt'
        ))

    def test_match_simple_patterns_direct_match(self):
        """
        Test simple relative tree pattern match case
        """
        patterns = (
            'filename.txt',
            '*/*.txt',
        )
        self.assertTrue(match_path_patterns(
            patterns,
            '/test',
            '/test/other files/filename.txt'
        ))

    def test_match_simple_patterns(self):
        """
        Test simple relative tree pattern match case
        """
        patterns = (
            'filename.wav',
            '*/*.txt',
        )
        self.assertTrue(match_path_patterns(
            patterns,
            '/test',
            '/test/other files/filename.txt'
        ))

    def test_match_prefix_match(self):
        """
        Test simple relative tree pattern match case
        """
        patterns = (
            'other files/*.txt',
        )
        self.assertTrue(match_path_patterns(
            patterns,
            '/test',
            '/test/other files/filename.txt'
        ))

    def test_match_prefix_glob_match(self):
        """
        Test simple relative tree pattern match case
        """
        patterns = (
            '*/other files/*',
        )
        self.assertTrue(match_path_patterns(
            patterns,
            '/test',
            '/test/data/other files/deeper/filename.txt'
        ))

    def test_match_relative_pattern(self):
        patterns = (
            'other */*.wav',
            '*/*.txt',
        )
        self.assertTrue(match_path_patterns(
            patterns,
            '/test/data',
            '/test/data/other files/filename.txt'
        ))
