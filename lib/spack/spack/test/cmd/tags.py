# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.cmd.install

from spack.main import SpackCommand

install = SpackCommand('install')
tags = SpackCommand('tags')


def test_tag_available(mock_packages, capfd):
    with capfd.disabled():
        out = tags()
        for tag in ['tag1', 'tag2', 'tag3']:
            assert tag in out


def test_tag_installed(mock_packages, capfd):
    with capfd.disabled():
        out = tags('-i')
        assert 'None' in out


@pytest.mark.parametrize('args,packages', [
    (('tag1',), ['mpich', 'mpich2']),
    (('tag2',), ['mpich']),
    (('tag3',), ['mpich2']),
    (('nosuchpackage',), ['None']),
    (('-s',), ['mpich2']),               # show available packages
    (('-i', 'tag2',), ['No installed'])  #
])
def test_tag_packages(args, packages, mock_packages):
    output = tags(*args)
    for pkg in packages:
        assert pkg in output


def test_tag_install_prob(
    mock_packages, mock_archive, mock_fetch, install_mockery, capfd
):
    install('mpich')
    with capfd.disabled():
        out = tags('', fail_on_error=False)

    assert 'See test log' in out
