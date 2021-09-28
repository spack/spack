# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import llnl.util.filesystem as fs

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


def test_do_test(mock_packages, mock_test_stage, install_mockery):
    """Perform a stand-alone test with files to copy."""
    spec = spack.spec.Spec('trivial-smoke-test').concretized()
    test_name = 'test_do_test'
    test_filename = 'test_file.in'

    pkg = spec.package
    pkg.create_extra_test_source()

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.current_test_spec = spec
    test_suite.current_base_spec = spec
    test_suite.ensure_stage()

    # Save off target paths for current spec since test suite processing
    # assumes testing multiple specs.
    cached_filename = fs.join_path(test_suite.current_test_cache_dir,
                                   pkg.test_source_filename)
    data_filename = fs.join_path(test_suite.current_test_data_dir,
                                 test_filename)

    # Run the test, making sure to retain the test stage directory
    # so we can ensure the files were copied.
    test_suite(remove_directory=False)

    assert os.path.exists(cached_filename)
    assert os.path.exists(data_filename)
