"""
Constants for 'treesync' utility
"""

from pathlib import Path

#: Default paths to look for configuration files
DEFAULT_CONFIGURATION_PATHS = (
    Path('~/.config/treesync.yml').expanduser(),
)

#: Filename in source directory automatically added as rsync exclude
DEFAULT_EXCLUDES_FILE = '.rsync.exclude'

#: Default excluded filenames and directories
DEFAULT_EXCLUDES = [
    '.pytest_cache/',
    '__pycache__/',
    '*.egg-info/',
    '*.pyc',
    '.*.swp',
    '*~',
]

#: Default flags for rsync
DEFAULT_FLAGS = [
    '--archive',
    '--verbose',
    '--delete',
]


#: Tree specific automatically loaded configuration file in source tree
TREE_CONFIG_FILE = '.treesync.yml'