
from systematic_cli.tests import validate_version_string

from systematic_files import __version__


def test_version_string():
    """
    Test format of module version string
    """
    validate_version_string(__version__)
