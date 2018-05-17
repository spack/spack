##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
        ('optional-dep-test', {'optional-dep-test': None}),
        ('optional-dep-test~a', {'optional-dep-test~a': None}),
        ('optional-dep-test+a', {'optional-dep-test+a': {'a': None}}),
        ('optional-dep-test a=true', {
            'optional-dep-test a=true': {
                'a': None
            }}),
        ('optional-dep-test a=true', {
            'optional-dep-test+a': {
                'a': None
            }}),
        ('optional-dep-test@1.1', {'optional-dep-test@1.1': {'b': None}}),
        ('optional-dep-test%intel', {'optional-dep-test%intel': {'c': None}}),
        ('optional-dep-test%intel@64.1', {
            'optional-dep-test%intel@64.1': {
                'c': None,
                'd': None
            }}),
        ('optional-dep-test%intel@64.1.2', {
            'optional-dep-test%intel@64.1.2': {
                'c': None,
                'd': None
            }}),
        ('optional-dep-test%clang@35', {
            'optional-dep-test%clang@35': {
                'e': None
            }}),
        # Normalize multiple conditionals
        ('optional-dep-test+a@1.1', {
            'optional-dep-test+a@1.1': {
                'a': None,
                'b': None
            }}),
        ('optional-dep-test+a%intel', {
            'optional-dep-test+a%intel': {
                'a': None,
                'c': None
            }}),
        ('optional-dep-test@1.1%intel', {
            'optional-dep-test@1.1%intel': {
                'b': None,
                'c': None
            }}),
        ('optional-dep-test@1.1%intel@64.1.2+a', {
            'optional-dep-test@1.1%intel@64.1.2+a': {
                'a': None,
                'b': None,
                'c': None,
                'd': None
            }}),
        ('optional-dep-test@1.1%clang@36.5+a', {
            'optional-dep-test@1.1%clang@36.5+a': {
                'b': None,
                'a': None,
                'e': None
            }}),
        # Chained MPI
        ('optional-dep-test-2+mpi', {
            'optional-dep-test-2+mpi': {
                'optional-dep-test+mpi': {'mpi': None}
            }}),
        # Each of these dependencies comes from a conditional
        # dependency on another.  This requires iterating to evaluate
        # the whole chain.
        ('optional-dep-test+f', {
            'optional-dep-test+f': {
                'f': None,
                'g': None,
                'mpi': None
            }})
    ]
)
def spec_and_expected(request):
    """Parameters for the normalization test."""
    spec, d = request.param
    return spec, Spec.from_literal(d)


def test_normalize(spec_and_expected, config, mock_packages):
    spec, expected = spec_and_expected
    spec = Spec(spec)
    spec.normalize()
    assert spec.eq_dag(expected, deptypes=False)


def test_default_variant(config, mock_packages):
    spec = Spec('optional-dep-test-3')
    spec.concretize()
    assert 'a' in spec

    spec = Spec('optional-dep-test-3~var')
    spec.concretize()
    assert 'a' in spec

    spec = Spec('optional-dep-test-3+var')
    spec.concretize()
    assert 'b' in spec
