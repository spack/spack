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

import spack.spec
from spack.main import SpackCommand

pytestmark = pytest.mark.usefixtures('config', 'mutable_mock_packages')

spec = SpackCommand('spec')


def test_spec():
    output = spec('mpileaks')

    assert 'mpileaks@2.3' in output
    assert 'callpath@1.0' in output
    assert 'dyninst@8.2' in output
    assert 'libdwarf@20130729' in output
    assert 'libelf@0.8.1' in output
    assert 'mpich@3.0.4' in output


def test_spec_yaml():
    output = spec('--yaml', 'mpileaks')

    mpileaks = spack.spec.Spec.from_yaml(output)
    assert 'mpileaks' in mpileaks
    assert 'callpath' in mpileaks
    assert 'dyninst' in mpileaks
    assert 'libdwarf' in mpileaks
    assert 'libelf' in mpileaks
    assert 'mpich' in mpileaks


def _parse_types(string):
    """Parse deptypes for specs from `spack spec -t` output."""
    lines = string.strip().split('\n')

    result = {}
    for line in lines:
        match = re.match(r'\[([^]]*)\]\s*\^?([^@]*)@', line)
        if match:
            types, name = match.groups()
            result.setdefault(name, []).append(types)
            result[name] = sorted(result[name])
    return result


def test_spec_deptypes_nodes():
    output = spec('--types', '--cover', 'nodes', 'dt-diamond')
    types = _parse_types(output)

    assert types['dt-diamond']        == ['    ']
    assert types['dt-diamond-left']   == ['bl  ']
    assert types['dt-diamond-right']  == ['bl  ']
    assert types['dt-diamond-bottom'] == ['blr ']


def test_spec_deptypes_edges():
    output = spec('--types', '--cover', 'edges', 'dt-diamond')
    types = _parse_types(output)

    assert types['dt-diamond']        == ['    ']
    assert types['dt-diamond-left']   == ['bl  ']
    assert types['dt-diamond-right']  == ['bl  ']
    assert types['dt-diamond-bottom'] == ['b   ', 'blr ']


def test_spec_returncode():
    with pytest.raises(spack.main.SpackCommandError):
        spec()
    assert spec.returncode == 1
