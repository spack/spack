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
"""Tests for provider index cache files.

Tests assume that mock packages provide this::

  {'blas':   {
       blas: set([netlib-blas, openblas, openblas-with-lapack])},
   'lapack': {lapack: set([netlib-lapack, openblas-with-lapack])},
   'mpi': {mpi@:1: set([mpich@:1]),
                    mpi@:2.0: set([mpich2]),
                    mpi@:2.1: set([mpich2@1.1:]),
                    mpi@:2.2: set([mpich2@1.2:]),
                    mpi@:3: set([mpich@3:]),
                    mpi@:10.0: set([zmpi])},
    'stuff': {stuff: set([externalvirtual])}}
"""
from six import StringIO

import spack
from spack.provider_index import ProviderIndex
from spack.spec import Spec


def test_yaml_round_trip(builtin_mock):
    p = ProviderIndex(spack.repo.all_package_names())

    ostream = StringIO()
    p.to_yaml(ostream)

    istream = StringIO(ostream.getvalue())
    q = ProviderIndex.from_yaml(istream)

    assert p == q


def test_providers_for_simple(builtin_mock):
    p = ProviderIndex(spack.repo.all_package_names())

    blas_providers = p.providers_for('blas')
    assert Spec('netlib-blas') in blas_providers
    assert Spec('openblas') in blas_providers
    assert Spec('openblas-with-lapack') in blas_providers

    lapack_providers = p.providers_for('lapack')
    assert Spec('netlib-lapack') in lapack_providers
    assert Spec('openblas-with-lapack') in lapack_providers


def test_mpi_providers(builtin_mock):
    p = ProviderIndex(spack.repo.all_package_names())

    mpi_2_providers = p.providers_for('mpi@2')
    assert Spec('mpich2') in mpi_2_providers
    assert Spec('mpich@3:') in mpi_2_providers

    mpi_3_providers = p.providers_for('mpi@3')
    assert Spec('mpich2') not in mpi_3_providers
    assert Spec('mpich@3:') in mpi_3_providers
    assert Spec('zmpi') in mpi_3_providers


def test_equal(builtin_mock):
    p = ProviderIndex(spack.repo.all_package_names())
    q = ProviderIndex(spack.repo.all_package_names())
    assert p == q


def test_copy(builtin_mock):
    p = ProviderIndex(spack.repo.all_package_names())
    q = p.copy()
    assert p == q
