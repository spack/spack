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

dependents = SpackCommand('dependents')


def test_immediate_dependents(mock_packages):
    out = dependents('libelf')
    actual = set(re.split(r'\s+', out.strip()))
    assert actual == set(['dyninst', 'libdwarf',
                          'patch-a-dependency', 'patch-several-dependencies'])


def test_transitive_dependents(mock_packages):
    out = dependents('--transitive', 'libelf')
    actual = set(re.split(r'\s+', out.strip()))
    assert actual == set(
        ['callpath', 'dyninst', 'libdwarf', 'mpileaks', 'multivalue_variant',
         'singlevalue-variant-dependent',
         'patch-a-dependency', 'patch-several-dependencies'])


@pytest.mark.db
def test_immediate_installed_dependents(mock_packages, database):
    with color_when(False):
        out = dependents('--installed', 'libelf')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['dyninst', 'libdwarf']])

    libelf = spack.store.db.query_one('libelf')
    expected = set([d.dag_hash(7) for d in libelf.dependents()])

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependents(mock_packages, database):
    with color_when(False):
        out = dependents('--installed', '--transitive', 'fake')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['zmpi', 'callpath^zmpi', 'mpileaks^zmpi']])

    assert expected == hashes
