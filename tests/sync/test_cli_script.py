
import pathlib
import sys

import pytest

from systematic_cli.test_validators.script import (
    validate_script_attributes,
    validate_script_run_exception_with_args,

)

from systematic_files.bin.treesync.main import main, Treesync
from systematic_files.tree import Tree

from . import TEST_DATA
from .utils import create_source_directory

EXCLUDES_FILE = TEST_DATA.joinpath('rsync.exclude')

DEFAULT_ARGS = {
    'debug': False,
    'quiet': False
}


def test_cli_treesync_run_main():
    """
    Run main() for treesync command without arguments
    """
    with pytest.raises(SystemExit):
        main()


def test_cli_treesync_attributes():
    """
    Validate basic attributes of treesync script
    """
    expected_args = DEFAULT_ARGS.copy()
    expected_args['test-cli_command'] = None
    validate_script_attributes(Treesync(), expected_args=expected_args)


def test_cli_treesync_pull_no_targets(monkeypatch):
    """
    Test running 'treesync pull' without targets
    """
    script = Treesync()
    testargs = ['treesync', 'pull']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_cli_treesync_pull_invalid_targets(monkeypatch):
    """
    Test running 'treesync push' with invalid targets
    """
    script = Treesync()
    testargs = ['treesync', 'pull', 'invalid-target-name']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_cli_treesync_push_no_targets(monkeypatch):
    """
    Test running 'treesync push' without targets
    """
    script = Treesync()
    testargs = ['treesync', 'push']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_cli_treesync_push_invalid_targets(monkeypatch):
    """
    Test running 'treesync push' with invalid targets
    """
    script = Treesync()
    testargs = ['treesync', 'push', 'invalid-target-name']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_cli_push_pull_tmpdir(tmpdir, monkeypatch):
    """
    Test pull and push with tmpdir
    """
    source, destination, config_file = create_source_directory(tmpdir, EXCLUDES_FILE)

    assert source.exists()
    assert not destination.exists()

    Tree(destination.parent).create()
    script = Treesync()

    testargs = ['treesync', 'push', '--config', str(config_file), 'test']
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        script.run()
    assert pathlib.Path(destination).exists()

    testargs = ['treesync', 'pull', '--config', str(config_file), 'test']
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        script.run()
