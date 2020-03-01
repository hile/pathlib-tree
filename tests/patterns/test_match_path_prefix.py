
import unittest

from systematic_files.patterns import match_path_prefix


class TestMatchPathPrefixes(unittest.TestCase):
    """
    Test the patch prefix match utility pattern method
    """

    def test_match_path_prefix_full_path(self):
        """
        Test matching path prefixes returns True
        """
        self.assertTrue(match_path_prefix('/test', '/test/other directory/filename.txt'))

    def test_match_path_prefix_components(self):
        """
        Test matching path prefixes returns True
        """
        self.assertTrue(match_path_prefix(
            ['test'],
            ['test', 'other directory', 'filename.txt']
        ))

    def test_match_path_prefix_full_path_no_match(self):
        """
        Test matching different path prefixes returns False
        """
        self.assertFalse(match_path_prefix('/test', '/testing/other directory/filename.txt'))

    def test_match_path_prefix_patterns(self):
        """
        Test matching different path prefixes returns False
        """
        self.assertTrue(match_path_prefix(
            '/test/*/filename.txt',
            '/test/other directory/filename.txt')
        )
        self.assertTrue(match_path_prefix(
            '/*/*/*.txt',
            '/test/other directory/filename.txt')
        )
        self.assertTrue(match_path_prefix(
            '/test/*',
            '/test/other directory/filename.txt')
        )

    def test_match_path_prefix_patterns_no_match(self):
        """
        Test matching different path prefixes returns False
        """
        self.assertFalse(match_path_prefix(
            '/test/mydata*/*.txt',
            '/test/other directory/filename.txt')
        )
        self.assertFalse(match_path_prefix(
            '/test/*',
            '/test')
        )
