# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import multiprocessing

import pytest


import spack.cmd.common.arguments as arguments


@pytest.fixture()
def parser():
    return argparse.ArgumentParser()


def test_setting_parallel_jobs(parser):
    arguments.add_common_arguments(parser, ['jobs'])

    # A negative integer has no meaning and raises an exception
    with pytest.raises(ValueError) as exc_info:
        parser.parse_args(['-j', '-2'])

    assert 'expected a positive integer' in str(exc_info.value)

    # Check that the default value is computed correctly
    ncpus = multiprocessing.cpu_count()
    namespace = parser.parse_args([])
    assert namespace.jobs == ncpus

    # Check that a positive integer works as expected
    namespace = parser.parse_args(['-j', '24'])
    assert namespace.jobs == 24
