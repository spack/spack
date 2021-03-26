# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import pytest

import spack.spec
from spack.main import SpackCommand

pytestmark = pytest.mark.usefixtures('config', 'mutable_mock_repo')

spec = SpackCommand('spec')


def test_spec(capsys):
    output = spec('mpileaks', out=capsys)

    assert 'mpileaks@2.3' in output
    assert 'callpath@1.0' in output
    assert 'dyninst@8.2' in output
    assert 'libdwarf@20130729' in output
    assert 'libelf@0.8.1' in output
    assert 'mpich@3.0.4' in output


def test_spec_yaml(capsys):
    output = spec('--yaml', 'mpileaks', out=capsys)

    mpileaks = spack.spec.Spec.from_yaml(output)
    assert 'mpileaks' in mpileaks
    assert 'callpath' in mpileaks
    assert 'dyninst' in mpileaks
    assert 'libdwarf' in mpileaks
    assert 'libelf' in mpileaks
    assert 'mpich' in mpileaks


def test_spec_json(capsys):
    output = spec('--json', 'mpileaks', out=capsys)

    mpileaks = spack.spec.Spec.from_json(output)
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


def test_spec_deptypes_nodes(capsys):
    output = spec('--types', '--cover', 'nodes', 'dt-diamond', out=capsys)
    types = _parse_types(output)

    assert types['dt-diamond']        == ['    ']
    assert types['dt-diamond-left']   == ['bl  ']
    assert types['dt-diamond-right']  == ['bl  ']
    assert types['dt-diamond-bottom'] == ['blr ']


def test_spec_deptypes_edges(capsys):
    output = spec('--types', '--cover', 'edges', 'dt-diamond', out=capsys)
    types = _parse_types(output)

    assert types['dt-diamond']        == ['    ']
    assert types['dt-diamond-left']   == ['bl  ']
    assert types['dt-diamond-right']  == ['bl  ']
    assert types['dt-diamond-bottom'] == ['b   ', 'blr ']


def test_spec_returncode():
    with pytest.raises(spack.main.SpackCommandError):
        spec()
    assert spec.returncode == 1
