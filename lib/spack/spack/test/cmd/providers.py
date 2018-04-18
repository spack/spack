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

from spack.main import SpackCommand

providers = SpackCommand('providers')


@pytest.mark.parametrize('pkg', [
    ('mpi',),
    ('mpi@2',),
    ('mpi', 'lapack'),
    ('',)  # Lists all the available virtual packages
])
def test_it_just_runs(pkg):
    providers(*pkg)


@pytest.mark.parametrize('vpkg,provider_list', [
    (('mpi',), ['intel-mpi',
                'intel-parallel-studio',
                'mpich',
                'mpich@1:',
                'mpich@3:',
                'mvapich2',
                'openmpi',
                'openmpi@1.6.5',
                'openmpi@1.7.5:',
                'openmpi@2.0.0:',
                'spectrum-mpi']),
    (('D', 'awk'), ['ldc', 'gawk', 'mawk'])  # Call 2 virtual packages at once
])
def test_provider_lists(vpkg, provider_list):
    output = providers(*vpkg)
    for item in provider_list:
        assert item in output


@pytest.mark.parametrize('pkg,error_cls', [
    ('zlib', ValueError),
    ('foo', ValueError)  # Trying to call with a package that does not exist
])
def test_it_just_fails(pkg, error_cls):
    with pytest.raises(error_cls):
        providers(pkg)
