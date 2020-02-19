##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.main

spack_filter = spack.main.SpackCommand('filter')


@pytest.mark.db
@pytest.mark.usefixtures('database')
@pytest.mark.parametrize('flags,specs,expected', [
    ([], ['boost', 'mpileaks'], ['boost', 'mpileaks']),
    (['--installed'],
     ['boost', 'mpileaks^mpich', 'libelf'],
     ['mpileaks^mpich', 'libelf']),
    (['--not-installed'], ['boost', 'mpileaks^mpich', 'libelf'], ['boost']),
    # The tests below appear to fail for reasons related to mocking
    pytest.param(
        ['--installed', '--explicit'],
        ['boost', 'mpileaks^mpich', 'libelf'], ['mpileaks^mpich'],
        marks=pytest.mark.xfail
    ),
    pytest.param(
        ['--implicit'],
        ['boost', 'mpileaks^mpich', 'libelf'], ['boost', 'libelf'],
        marks=pytest.mark.xfail
    ),
])
def test_filtering_specs(flags, specs, expected):
    args = flags + specs
    output = spack_filter(*args)

    for item in expected:
        assert item in output

    for item in set(specs).difference(expected):
        assert item not in output
