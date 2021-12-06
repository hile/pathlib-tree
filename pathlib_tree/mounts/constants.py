"""
Constants for parsing OS family specific mount and usage line outputs
"""

import re

GNU_MOUNT_COMMAND = ('mount',)
# Patterns to match lines from GNU based 'mount' command
RE_GNU_MOUNT_LINE = [
    re.compile(
        # pylint: disable=consider-using-f-string
        r'^{}$'.format(
            r'\s+'.join([
                r'(?P<device>[^\s]*) on',
                r'(?P<mountpoint>[^\s]*) type',
                r'(?P<filesystem>[^\s]*)',
                r'\((?P<options>[^\)]*)\)'
            ])
        )
    )
]
BSD_MOUNT_COMMAND = ('mount',)
# Patterns to match lines from BSD 'mount' output
RE_BSD_MOUNT_LINE = [
    re.compile(
        # pylint: disable=consider-using-f-string
        r'^{}$'.format(
            r'\s+'.join([
                r'(?P<device>[^\s]*) on',
                r'(?P<mountpoint>[^\s]*)',
                r'\((?P<options>[^\)]*)\)'
            ])
        )
    )
]

GNU_DF_COMMAND = ('df', '-Pk')
# Patterns to match lines from GNU based 'df -Pk' output
RE_GNU_DF_LINE = [
    re.compile(
        # pylint: disable=consider-using-f-string
        r'^{}$'.format(
            r'\s+'.join([
                r'(?P<device>[^\s]*)',
                r'(?P<size>\d+)',
                r'(?P<used>\d+)',
                r'(?P<available>\d+)',
                r'(?P<percent>\d+)%',
                r'(?P<mountpoint>.*)',
            ])
        )
    )
]

BSD_DF_COMMAND = ('df', '-Pki')
# Patterns to match lines from BSD based 'df -Pki' output
RE_BSD_DF_LINE = [
    re.compile(
        # pylint: disable=consider-using-f-string
        r'^{}$'.format(
            r'\s+'.join([
                r'(?P<device>[^\s]*)',
                r'(?P<size>\d+)',
                r'(?P<used>\d+)',
                r'(?P<available>\d+)',
                r'(?P<percent>\d+)%',
                r'(?P<inodes_used>\d+)',
                r'(?P<inodes_available>\d+)',
                r'(?P<inodes_percent>\d+)%',
                r'(?P<mountpoint>.*)',
            ])
        )
    )
]
