
import fnmatch
import os

from pathlib import Path


def match_path_prefix(prefix, path):
    """
    Match path prefix for two paths with fnmatch applied to path components
    """
    if isinstance(prefix, str):
        prefix = prefix.split(os.sep)
    if isinstance(path, str):
        path = path.split(os.sep)

    for index, path_pattern in enumerate(prefix):
        if index > len(path) - 1:
            return False
        if not fnmatch.fnmatch(path[index], path_pattern):
            return False
    return True


def match_path_patterns(patterns, root, path):
    """
    Match specified path to filename patterns compared to root directory
    """
    filename = os.path.basename(path)
    try:
        relative_path = str(Path(path).relative_to(root))
    except ValueError:
        relative_path = None

    for pattern in patterns:
        # Filename direct pattern match
        if relative_path == pattern or fnmatch.fnmatch(filename, pattern):
            return True

        # Match relative path to pattern
        if relative_path is not None and fnmatch.fnmatch(relative_path, pattern):
            return True

    return False
