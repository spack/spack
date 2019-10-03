# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import contextlib
import os.path

import jsonschema

import llnl.util.cpu
import llnl.util.cpu.detect

import spack.paths

# This is needed to check that with repr we could create equivalent objects
from llnl.util.cpu import Microarchitecture  # noqa


@pytest.fixture(params=[
    'linux-ubuntu18.04-broadwell',
    'linux-rhel7-broadwell',
    'linux-rhel7-skylake_avx512',
    'linux-rhel7-ivybridge',
    'linux-rhel7-haswell',
    'linux-rhel7-zen',
    'linux-rhel6-piledriver',
    'linux-centos7-power8le',
    'darwin-mojave-ivybridge',
    'darwin-mojave-broadwell',
    'bgq-rhel6-power7'
])
def expected_target(request, monkeypatch):
    cpu = llnl.util.cpu
    platform, operating_system, target = request.param.split('-')

    architecture_family = llnl.util.cpu.targets[target].family
    monkeypatch.setattr(
        cpu.detect.platform, 'machine', lambda: str(architecture_family)
    )

    # Monkeypatch for linux
    if platform in ('linux', 'bgq'):
        monkeypatch.setattr(cpu.detect.platform, 'system', lambda: 'Linux')

        @contextlib.contextmanager
        def _open(not_used_arg):
            filename = os.path.join(
                spack.paths.test_path, 'data', 'targets', request.param
            )
            with open(filename) as f:
                yield f

        monkeypatch.setattr(cpu.detect, 'open', _open, raising=False)

    elif platform == 'darwin':
        monkeypatch.setattr(cpu.detect.platform, 'system', lambda: 'Darwin')

        filename = os.path.join(
            spack.paths.test_path, 'data', 'targets', request.param
        )
        info = {}
        with open(filename) as f:
            for line in f:
                key, value = line.split(':')
                info[key.strip()] = value.strip()

        def _check_output(args):
            current_key = args[-1]
            return info[current_key]

        monkeypatch.setattr(cpu.detect, 'check_output', _check_output)

    return llnl.util.cpu.targets[target]


@pytest.fixture(params=[x for x in llnl.util.cpu.targets])
def supported_target(request):
    return request.param


def test_target_detection(expected_target):
    detected_target = llnl.util.cpu.host()
    assert detected_target == expected_target


def test_no_dashes_in_target_names(supported_target):
    assert '-' not in supported_target


def test_str_conversion(supported_target):
    assert supported_target == str(llnl.util.cpu.targets[supported_target])


def test_repr_conversion(supported_target):
    target = llnl.util.cpu.targets[supported_target]
    assert eval(repr(target)) == target


def test_equality(supported_target):
    target = llnl.util.cpu.targets[supported_target]

    for name, other_target in llnl.util.cpu.targets.items():
        if name == supported_target:
            assert other_target == target
        else:
            assert other_target != target


@pytest.mark.parametrize('operation,expected_result', [
    # Test microarchitectures that are ordered with respect to each other
    ('x86_64 < skylake', True),
    ('icelake > skylake', True),
    ('piledriver <= steamroller', True),
    ('zen2 >= zen', True),
    ('zen >= zen', True),
    # Test unrelated microarchitectures
    ('power8 < skylake', False),
    ('power8 <= skylake', False),
    ('skylake < power8', False),
    ('skylake <= power8', False),
    # Test microarchitectures of the same family that are not a "subset"
    # of each other
    ('cascadelake > cannonlake', False),
    ('cascadelake < cannonlake', False),
    ('cascadelake <= cannonlake', False),
    ('cascadelake >= cannonlake', False),
    ('cascadelake == cannonlake', False),
    ('cascadelake != cannonlake', True)
])
def test_partial_ordering(operation, expected_result):
    target, operator, other_target = operation.split()
    target = llnl.util.cpu.targets[target]
    other_target = llnl.util.cpu.targets[other_target]
    code = 'target ' + operator + 'other_target'
    assert eval(code) is expected_result


@pytest.mark.parametrize('target_name,expected_family', [
    ('skylake', 'x86_64'),
    ('zen', 'x86_64'),
    ('pentium2', 'x86'),
])
def test_architecture_family(target_name, expected_family):
    target = llnl.util.cpu.targets[target_name]
    assert str(target.family) == expected_family


@pytest.mark.parametrize('target_name,feature', [
    ('skylake', 'avx2'),
    ('icelake', 'avx512f'),
    # Test feature aliases
    ('icelake', 'avx512'),
    ('skylake', 'sse3'),
    ('power8', 'altivec'),
    ('broadwell', 'sse4.1'),
])
def test_features_query(target_name, feature):
    target = llnl.util.cpu.targets[target_name]
    assert feature in target


@pytest.mark.parametrize('target_name,wrong_feature', [
    ('skylake', 1),
    ('bulldozer', llnl.util.cpu.targets['x86_64'])
])
def test_wrong_types_for_features_query(target_name, wrong_feature):
    target = llnl.util.cpu.targets[target_name]
    with pytest.raises(TypeError, match='only objects of string types'):
        assert wrong_feature in target


def test_generic_microarchitecture():
    generic_march = llnl.util.cpu.generic_microarchitecture('foo')

    assert generic_march.name == 'foo'
    assert not generic_march.features
    assert not generic_march.ancestors
    assert generic_march.vendor == 'generic'


def test_target_json_schema():
    # The file microarchitectures.json contains static data i.e. data that is
    # not meant to be modified by users directly. It is thus sufficient to
    # validate it only once during unit tests.
    json_data = llnl.util.cpu.schema.targets_json.data
    jsonschema.validate(json_data, llnl.util.cpu.schema.schema)


@pytest.mark.parametrize('target_name,compiler,version,expected_flags', [
    ('x86_64', 'gcc', '4.9.3', '-march=x86-64 -mtune=x86-64'),
    ('nocona', 'gcc', '4.9.3', '-march=nocona -mtune=nocona'),
    ('nehalem', 'gcc', '4.9.3', '-march=nehalem -mtune=nehalem'),
    ('nehalem', 'gcc', '4.8.5', '-march=corei7 -mtune=corei7'),
    ('sandybridge', 'gcc', '4.8.5', '-march=corei7-avx -mtune=corei7-avx'),
    # Test that an unknown compiler returns an empty string
    ('sandybridge', 'unknown', '4.8.5', ''),
])
def test_optimization_flags(target_name, compiler, version, expected_flags):
    target = llnl.util.cpu.targets[target_name]
    flags = target.optimization_flags(compiler, version)
    assert flags == expected_flags


@pytest.mark.parametrize('target_name,compiler,version', [
    ('excavator', 'gcc', '4.8.5')
])
def test_unsupported_optimization_flags(target_name, compiler, version):
    target = llnl.util.cpu.targets[target_name]
    with pytest.raises(
            llnl.util.cpu.UnsupportedMicroarchitecture,
            matches='cannot produce optimized binary'
    ):
        target.optimization_flags(compiler, version)


@pytest.mark.parametrize('operation,expected_result', [
    # In the tests below we won't convert the right hand side to
    # Microarchitecture, so that automatic conversion from a known
    # target name will be tested
    ('cascadelake > cannonlake', False),
    ('cascadelake < cannonlake', False),
    ('cascadelake <= cannonlake', False),
    ('cascadelake >= cannonlake', False),
    ('cascadelake == cannonlake', False),
    ('cascadelake != cannonlake', True)
])
def test_automatic_conversion_on_comparisons(operation, expected_result):
    target, operator, other_target = operation.split()
    target = llnl.util.cpu.targets[target]
    code = 'target ' + operator + 'other_target'
    assert eval(code) is expected_result
