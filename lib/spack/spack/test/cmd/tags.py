# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import pytest

import spack.repo

from spack.main import SpackCommand
from spack.spec import Spec

tags = SpackCommand('tags')


def test_tags_no_installed(install_mockery, mock_fetch):
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
def test_tags_packages(install_mockery, mock_fetch, args, packages):
    out = tags(*args)
    for pkg in packages:
        assert pkg in out


@pytest.mark.parametrize('package,options,outputs', [
    # Process available tags, so packages if showing or tags if not
    ('mpich', [], ['tag1', 'tag2']),                 # relevant tags
    ('mpich2', [], ['tag1', 'tag3']),                # relevant tags
    ('mpich', ['-s'], ['mpich', 'No installed']),    # installed or No installed

    # Process provided tags, so show installed package or No installed
    ('mpich', ['tag1', 'tag2'], ['mpich']) ,
    ('mpich', ['tag3'], ['No installed']),
    ('mpich2', ['tag1', 'tag3'], ['mpich2']) ,
    ('mpich2', ['tag2'], ['No installed']),
])
def test_tags_installed(
    install_mockery, mock_fetch, package, options, outputs
):
    spec = Spec(package).concretized()
    pkg = spack.repo.get(spec)
    pkg.do_install()

    args = ['-i'] + options
    out = tags(*args)
    for item in outputs:
        assert item in out

    if package == outputs[-1]:
        assert 'No installed' not in outputs
