##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import pytest
from spack.spec import Spec


@pytest.fixture(
    params=[
        # Normalize simple conditionals
        ('optional-dep-test', Spec('optional-dep-test')),
        ('optional-dep-test~a', Spec('optional-dep-test~a')),
        ('optional-dep-test+a', Spec('optional-dep-test+a', Spec('a'))),
        ('optional-dep-test a=true', Spec(
            'optional-dep-test a=true', Spec('a')
        )),
        ('optional-dep-test a=true', Spec('optional-dep-test+a', Spec('a'))),
        ('optional-dep-test@1.1', Spec('optional-dep-test@1.1', Spec('b'))),
        ('optional-dep-test%intel', Spec(
            'optional-dep-test%intel', Spec('c')
        )),
        ('optional-dep-test%intel@64.1', Spec(
            'optional-dep-test%intel@64.1', Spec('c'), Spec('d')
        )),
        ('optional-dep-test%intel@64.1.2', Spec(
            'optional-dep-test%intel@64.1.2', Spec('c'), Spec('d')
        )),
        ('optional-dep-test%clang@35', Spec(
            'optional-dep-test%clang@35', Spec('e')
        )),
        # Normalize multiple conditionals
        ('optional-dep-test+a@1.1',  Spec(
            'optional-dep-test+a@1.1', Spec('a'), Spec('b')
        )),
        ('optional-dep-test+a%intel', Spec(
            'optional-dep-test+a%intel', Spec('a'), Spec('c')
        )),
        ('optional-dep-test@1.1%intel', Spec(
            'optional-dep-test@1.1%intel', Spec('b'), Spec('c')
        )),
        ('optional-dep-test@1.1%intel@64.1.2+a', Spec(
            'optional-dep-test@1.1%intel@64.1.2+a',
            Spec('b'),
            Spec('a'),
            Spec('c'),
            Spec('d')
        )),
        ('optional-dep-test@1.1%clang@36.5+a', Spec(
            'optional-dep-test@1.1%clang@36.5+a',
            Spec('b'),
            Spec('a'),
            Spec('e')
        )),
        # Chained MPI
        ('optional-dep-test-2+mpi', Spec(
            'optional-dep-test-2+mpi',
            Spec('optional-dep-test+mpi', Spec('mpi'))
        )),
        # Each of these dependencies comes from a conditional
        # dependency on another.  This requires iterating to evaluate
        # the whole chain.
        ('optional-dep-test+f', Spec(
            'optional-dep-test+f', Spec('f'), Spec('g'), Spec('mpi')
        ))
    ]
)
def spec_and_expected(request):
    """Parameters for te normalization test."""
    return request.param


def test_normalize(spec_and_expected, config, builtin_mock):
    spec, expected = spec_and_expected
    spec = Spec(spec)
    spec.normalize()
    assert spec.eq_dag(expected, deptypes=False)


def test_default_variant(config, builtin_mock):
    spec = Spec('optional-dep-test-3')
    spec.concretize()
    assert 'a' in spec

    spec = Spec('optional-dep-test-3~var')
    spec.concretize()
    assert 'a' in spec

    spec = Spec('optional-dep-test-3+var')
    spec.concretize()
    assert 'b' in spec
