# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

import spack.environment as ev
import spack.spec
import spack.store
from spack.main import SpackCommand, SpackCommandError

pytestmark = pytest.mark.usefixtures('config', 'mutable_mock_repo')

spec = SpackCommand('spec')

base32_alphabet = 'abcdefghijklmnopqrstuvwxyz234567'


def test_spec():
    output = spec('mpileaks')

    assert 'mpileaks@2.3' in output
    assert 'callpath@1.0' in output
    assert 'dyninst@8.2' in output
    assert 'libdwarf@20130729' in output
    assert 'libelf@0.8.1' in output
    assert 'mpich@3.0.4' in output


def test_spec_concretizer_args(mutable_config, mutable_database):
    """End-to-end test of CLI concretizer prefs.

    It's here to make sure that everything works from CLI
    options to `solver.py`, and that config options are not
    lost along the way.
    """
    if spack.config.get('config:concretizer') == 'original':
        pytest.xfail('Known failure of the original concretizer')

    # remove two non-preferred mpileaks installations
    # so that reuse will pick up the zmpi one
    uninstall = SpackCommand("uninstall")
    uninstall("-y", "mpileaks^mpich")
    uninstall("-y", "mpileaks^mpich2")

    # get the hash of mpileaks^zmpi
    mpileaks_zmpi = spack.store.db.query_one("mpileaks^zmpi")
    h = mpileaks_zmpi.dag_hash()[:7]

    output = spec("--fresh", "-l", "mpileaks")
    assert h not in output

    output = spec("--reuse", "-l", "mpileaks")
    assert h in output


def test_spec_yaml():
    output = spec('--yaml', 'mpileaks')

    mpileaks = spack.spec.Spec.from_yaml(output)
    assert 'mpileaks' in mpileaks
    assert 'callpath' in mpileaks
    assert 'dyninst' in mpileaks
    assert 'libdwarf' in mpileaks
    assert 'libelf' in mpileaks
    assert 'mpich' in mpileaks


def test_spec_json():
    output = spec('--json', 'mpileaks')

    mpileaks = spack.spec.Spec.from_json(output)
    assert 'mpileaks' in mpileaks
    assert 'callpath' in mpileaks
    assert 'dyninst' in mpileaks
    assert 'libdwarf' in mpileaks
    assert 'libelf' in mpileaks
    assert 'mpich' in mpileaks


def test_spec_format(database, config):
    output = spec('--format', '{name}-{^mpi.name}', 'mpileaks')
    assert output.rstrip('\n') == "mpileaks-mpich"

    output = spec('--format', '{name}-{version}-{compiler.name}-{^mpi.name}',
                  'mpileaks')
    assert "installed package" not in output
    assert output.rstrip('\n') == "mpileaks-2.3-gcc-mpich"

    output = spec('--format', '{name}-{^mpi.name}-{hash:7}',
                  'mpileaks')
    output = output.rstrip('\n')
    assert output[:-7] == "mpileaks-mpich-"

    # hashes are in base32
    for c in output[-7:]:
        assert c in base32_alphabet


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
    with pytest.raises(SpackCommandError):
        spec()
    assert spec.returncode == 1


def test_env_aware_spec(mutable_mock_env_path):
    env = ev.create('test')
    env.add('mpileaks')

    with env:
        output = spec()
        assert 'mpileaks@2.3' in output
        assert 'callpath@1.0' in output
        assert 'dyninst@8.2' in output
        assert 'libdwarf@20130729' in output
        assert 'libelf@0.8.1' in output
        assert 'mpich@3.0.4' in output
