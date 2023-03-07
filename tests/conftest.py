#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Pytest configuration for all tests
"""
from pathlib import Path
from typing import Iterator, List

import pytest

MOCK_DATA = Path(__file__).parent.joinpath('mock')


@pytest.fixture(autouse=True)
def common_fixtures(cli_mock_argv) -> Iterator[List[str]]:
    """
    Wrap cli_mock_argv to be used in all tests
    """
    yield cli_mock_argv
