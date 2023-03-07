#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit test configuration pathlib_tree.tree
"""
import sys

from pathlib import Path
from typing import Iterator

import pytest

from sys_toolkit.tests.mock import MockException
from pathlib_tree import Tree

from ..conftest import MOCK_DATA

MOCK_TREE_A_PATH = MOCK_DATA.joinpath('tree/a')
MOCK_TREE_B_PATH = MOCK_DATA.joinpath('tree/b')
MOCK_TREE_DIFFERENT_COUNT = 1
MOCK_TREE_A_MISSING_COUNT = 3
MOCK_TREE_B_MISSING_COUNT = 4

TEST_DIRECTORY_DATA = [
    {
        'name': 'foo',
        'children': [
            'a',
            'b',
            'c'
        ],
    },
    {
        'name': 'bar',
        'children': [
            'aa.tst',
            'bb.tst',
            'cc.tst',
            {
                'name': 'baz',
                'children': [
                    'd.txt',
                    'dd.txt',
                    'ddd.txt',
                ]
            }
        ]
    }
]


@pytest.fixture
def mock_test_tree(tmpdir) -> Iterator[Path]:
    """
    Create test directory for filtering searches
    """
    def create_directory_items(prefix, item):
        path = Path(prefix, item['name'])
        path.mkdir(parents=True)
        for child in item.get('children', []):
            if isinstance(child, dict):
                create_directory_items(path, child)
            else:
                filename = path.joinpath(child)
                with filename.open('w', encoding='utf-8') as filedescriptor:
                    filedescriptor.write('\n')

    test_directory = Path(tmpdir.strpath, 'mock-test-directory')
    for item in TEST_DIRECTORY_DATA:
        create_directory_items(test_directory, item)
    yield test_directory


@pytest.fixture
def libmagic_import_error(monkeypatch) -> None:
    """
    Mock import error for magic library
    """
    monkeypatch.setitem(sys.modules, 'magic', None)


@pytest.fixture
def libmagic_call_error(monkeypatch) -> Iterator[MockException]:
    """
    Mock error calling magic library
    """
    mock_error = MockException(OSError)
    monkeypatch.setattr('magic.Magic.id_filename', mock_error)
    yield mock_error


@pytest.fixture
def parent_path() -> Iterator[str]:
    """
    Return parent directory of this file as string fixture
    """
    yield str(Path(__file__).parent.resolve())


@pytest.fixture
def tests_path() -> Iterator[str]:
    """
    Return tests directory directory of this file as string fixture
    """
    yield str(Path(__file__).parent.parent.resolve())


@pytest.fixture
def mock_tree_a() -> Iterator[Tree]:
    """
    Return mock tree A for tests
    """
    yield Tree(str(MOCK_TREE_A_PATH))


@pytest.fixture
def mock_tree_b() -> Iterator[Tree]:
    """
    Return mock tree B for tests
    """
    yield Tree(str(MOCK_TREE_B_PATH))
