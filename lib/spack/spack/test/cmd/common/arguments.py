# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import multiprocessing

import pytest


import spack.cmd.common.arguments as arguments
import spack.config


@pytest.fixture()
def parser():
    p = argparse.ArgumentParser()
    arguments.add_common_arguments(p, ['jobs'])
    yield p
    # Cleanup the command line scope if it was set during tests
    if 'command_line' in spack.config.config.scopes:
        spack.config.config.remove_scope('command_line')


@pytest.mark.parametrize('cli_args,expected', [
    (['-j', '24'], 24),
    ([], multiprocessing.cpu_count())
])
def test_setting_parallel_jobs(parser, cli_args, expected):
    namespace = parser.parse_args(cli_args)
    assert namespace.jobs == expected
    assert spack.config.get('config:build_jobs') == expected


def test_negative_integers_not_allowed_for_parallel_jobs(parser):
    with pytest.raises(ValueError) as exc_info:
        parser.parse_args(['-j', '-2'])

    assert 'expected a positive integer' in str(exc_info.value)
