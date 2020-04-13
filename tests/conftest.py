"""
Pytest configuration for all tests
"""

import os
import pathlib

import pytest

from systematic_files.sync.configuration import DEFAULT_CONFIGURATION_PATHS


@pytest.fixture(autouse=True)
def common_fixtures(cli_mock_argv):
    """
    Wrap cli_mock_argv to be used in all tests
    """
    print('mock CLI argv', cli_mock_argv)


@pytest.fixture(scope='module', autouse=True)
def mock_no_user__sync_config():
    """
    Mock user configuration path
    """

    def exists(self):
        if self in DEFAULT_CONFIGURATION_PATHS:
            return False
        return os.path.exists(str(self))

    def is_file(self):
        if self in DEFAULT_CONFIGURATION_PATHS:
            return False
        return os.path.isfile(str(self))

    # pylint: disable=import-outside-toplevel
    from _pytest.monkeypatch import MonkeyPatch
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(pathlib.Path, 'exists', exists)
    monkeypatch.setattr(pathlib.Path, 'is_file', is_file)

    yield monkeypatch
    monkeypatch.undo()
