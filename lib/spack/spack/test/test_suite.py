# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import spack.install_test
import spack.spec


def test_test_log_pathname(mock_packages, config):
    """Ensure test log path is reasonable."""
    spec = spack.spec.Spec('libdwarf').concretized()

    test_name = 'test_name'

    test_suite = spack.install_test.TestSuite([spec], test_name)
    logfile = test_suite.log_file_for_spec(spec)

    assert test_suite.stage in logfile
    assert test_suite.test_log_name(spec) in logfile


def test_test_ensure_stage(mock_test_stage):
    """Make sure test stage directory is properly set up."""
    spec = spack.spec.Spec('libdwarf').concretized()

    test_name = 'test_name'

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.ensure_stage()

    assert os.path.isdir(test_suite.stage)
    assert mock_test_stage in test_suite.stage


def test_write_test_result(mock_packages, mock_test_stage):
    """Ensure test results written to a results file."""
    spec = spack.spec.Spec('libdwarf').concretized()
    result = 'TEST'
    test_name = 'write-test'

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.ensure_stage()
    results_file = test_suite.results_file
    test_suite.write_test_result(spec, result)

    with open(results_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 1

        msg = lines[0]
        assert result in msg
        assert spec.name in msg
