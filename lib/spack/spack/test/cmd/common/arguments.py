# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import multiprocessing

import pytest


import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config


@pytest.fixture()
def job_parser():
    # --jobs needs to write to a command_line config scope, so this is the only
    # scope we create.
    p = argparse.ArgumentParser()
    arguments.add_common_arguments(p, ['jobs'])
    scopes = [spack.config.InternalConfigScope('command_line', {'config': {}})]

    with spack.config.use_configuration(*scopes):
        yield p


@pytest.mark.parametrize("ncores", [1, 2, 4, 8, 16, 32])
def test_setting_jobs_flag(job_parser, ncores, monkeypatch):
    monkeypatch.setattr(multiprocessing, 'cpu_count', lambda: ncores)
    namespace = job_parser.parse_args(['-j', '24'])
    expected = min(24, ncores)
    assert namespace.jobs == expected
    assert spack.config.get('config:build_jobs') == expected


@pytest.mark.parametrize("ncores", [1, 2, 4, 8, 16, 32])
def test_omitted_job_flag(job_parser, ncores, monkeypatch):
    monkeypatch.setattr(multiprocessing, 'cpu_count', lambda: ncores)
    namespace = job_parser.parse_args([])
    assert namespace.jobs == min(ncores, 16)
    assert spack.config.get('config:build_jobs') is None


def test_negative_integers_not_allowed_for_parallel_jobs(job_parser):
    with pytest.raises(ValueError) as exc_info:
        job_parser.parse_args(['-j', '-2'])

    assert 'expected a positive integer' in str(exc_info.value)


@pytest.mark.parametrize('specs,expected_variants,unexpected_variants', [
    (['coreutils', 'cflags=-O3 -g'], [], ['g']),
    (['coreutils', 'cflags=-O3', '-g'], ['g'], []),
])
@pytest.mark.regression('12951')
def test_parse_spec_flags_with_spaces(
        specs, expected_variants, unexpected_variants
):
    spec_list = spack.cmd.parse_specs(specs)
    assert len(spec_list) == 1

    s = spec_list.pop()

    assert all(x not in s.variants for x in unexpected_variants)
    assert all(x in s.variants for x in expected_variants)
