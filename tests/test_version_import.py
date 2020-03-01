
from systematic_cli.version import __version__


def test_version_string():
    """
    Test format of module version string
    """
    parts = __version__.split('.')
    for part in parts:
        assert int(part) >= 0
