# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import pytest
import re

import spack.main
import spack.repo

maintainers = spack.main.SpackCommand('maintainers')


def split(output):
    """Split command line output into an array."""
    output = output.strip()
    return re.split(r'\s+', output) if output else []


def test_maintained(mock_packages, capsys):
    out = split(maintainers('--maintained', out=capsys))
    assert out == ['maintainers-1', 'maintainers-2']


def test_unmaintained(mock_packages, capsys):
    out = split(maintainers('--unmaintained', out=capsys))
    assert out == sorted(
        set(spack.repo.all_package_names()) -
        set(['maintainers-1', 'maintainers-2']))


def test_all(mock_packages, capsys):
    out = split(maintainers('--all', out=capsys))
    assert out == [
        'maintainers-1:', 'user1,', 'user2',
        'maintainers-2:', 'user2,', 'user3',
    ]

    out = split(maintainers('--all', 'maintainers-1', out=capsys))
    assert out == [
        'maintainers-1:', 'user1,', 'user2',
    ]


def test_all_by_user(mock_packages, capsys):
    out = split(maintainers('--all', '--by-user', out=capsys))
    assert out == [
        'user1:', 'maintainers-1',
        'user2:', 'maintainers-1,', 'maintainers-2',
        'user3:', 'maintainers-2',
    ]

    out = split(maintainers('--all', '--by-user', 'user1', 'user2', out=capsys))
    assert out == [
        'user1:', 'maintainers-1',
        'user2:', 'maintainers-1,', 'maintainers-2',
    ]


def test_no_args(mock_packages):
    with pytest.raises(spack.main.SpackCommandError):
        maintainers()


def test_no_args_by_user(mock_packages):
    with pytest.raises(spack.main.SpackCommandError):
        maintainers('--by-user')


def test_mutex_args_fail(mock_packages):
    with pytest.raises(SystemExit):
        maintainers('--maintained', '--unmaintained')


def test_maintainers_list_packages(mock_packages, capsys):
    out = split(maintainers('maintainers-1', out=capsys))
    assert out == ['user1', 'user2']

    out = split(maintainers('maintainers-1', 'maintainers-2', out=capsys))
    assert out == ['user1', 'user2', 'user3']

    out = split(maintainers('maintainers-2', out=capsys))
    assert out == ['user2', 'user3']


def test_maintainers_list_fails(mock_packages, capsys):
    out = maintainers('a', fail_on_error=False, out=capsys)
    assert not out
    assert maintainers.returncode == 1


def test_maintainers_list_by_user(mock_packages, capsys):
    out = split(maintainers('--by-user', 'user1', out=capsys))
    assert out == ['maintainers-1']

    out = split(maintainers('--by-user', 'user1', 'user2', out=capsys))
    assert out == ['maintainers-1', 'maintainers-2']

    out = split(maintainers('--by-user', 'user2', out=capsys))
    assert out == ['maintainers-1', 'maintainers-2']

    out = split(maintainers('--by-user', 'user3', out=capsys))
    assert out == ['maintainers-2']
