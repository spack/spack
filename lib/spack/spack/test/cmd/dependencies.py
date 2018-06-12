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
import re
import pytest

from llnl.util.tty.color import color_when

import spack.store
from spack.main import SpackCommand

dependencies = SpackCommand('dependencies')

mpis = ['mpich', 'mpich2', 'multi-provider-mpi', 'zmpi']
mpi_deps = ['fake']


def test_immediate_dependencies(mock_packages):
    out = dependencies('mpileaks')
    actual = set(re.split(r'\s+', out.strip()))
    expected = set(['callpath'] + mpis)
    assert expected == actual


def test_transitive_dependencies(mock_packages):
    out = dependencies('--transitive', 'mpileaks')
    actual = set(re.split(r'\s+', out.strip()))
    expected = set(
        ['callpath', 'dyninst', 'libdwarf', 'libelf'] + mpis + mpi_deps)
    assert expected == actual


@pytest.mark.db
def test_immediate_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies('--installed', 'mpileaks^mpich')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['mpich', 'callpath^mpich']])

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies('--installed', '--transitive', 'mpileaks^zmpi')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['zmpi', 'callpath^zmpi', 'fake',
                              'dyninst', 'libdwarf', 'libelf']])

    assert expected == hashes
