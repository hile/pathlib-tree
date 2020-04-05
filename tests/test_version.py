
from systematic_files import __version__
from systematic_cli.tests import validate_version_string


def test_version_string():
    """
    Test format of module version string
    """
    validate_version_string(__version__)
