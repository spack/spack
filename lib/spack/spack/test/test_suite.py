# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

import pytest

import llnl.util.filesystem as fs

import spack.install_test
import spack.spec


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_test_log_pathname(mock_packages, config):
    """Ensure test log path is reasonable."""
    spec = spack.spec.Spec('libdwarf').concretized()

    test_name = 'test_name'

    test_suite = spack.install_test.TestSuite([spec], test_name)
    logfile = test_suite.log_file_for_spec(spec)

    assert test_suite.stage in logfile
    assert test_suite.test_log_name(spec) in logfile


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_test_ensure_stage(mock_test_stage):
    """Make sure test stage directory is properly set up."""
    spec = spack.spec.Spec('libdwarf').concretized()

    test_name = 'test_name'

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.ensure_stage()

    assert os.path.isdir(test_suite.stage)
    assert mock_test_stage in test_suite.stage


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
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


@pytest.mark.skipif(sys.platform == 'win32', reason="Not yet implemented on windows")
def test_do_test(mock_packages, install_mockery, mock_test_stage):
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


@pytest.mark.parametrize('arguments,status,msg', [
    ({}, 'SKIPPED', 'Skipped'),
    ({'externals': True}, 'NO-TESTS', 'No tests'),
])
def test_test_external(mock_packages, install_mockery, mock_test_stage,
                       arguments, status, msg):
    def ensure_results(filename, expected):
        assert os.path.exists(filename)
        with open(filename, 'r') as fd:
            lines = fd.readlines()
            have = False
            for line in lines:
                if expected in line:
                    have = True
                    break
            assert have

    name = 'trivial-smoke-test'
    spec = spack.spec.Spec(name).concretized()
    spec.external_path = '/path/to/external/{0}'.format(name)

    test_suite = spack.install_test.TestSuite([spec])
    test_suite(**arguments)

    ensure_results(test_suite.results_file, status)
    ensure_results(test_suite.log_file_for_spec(spec), msg)


def test_test_stage_caches(mock_packages, install_mockery, mock_test_stage):
    def ensure_current_cache_fail(test_suite):
        with pytest.raises(spack.install_test.TestSuiteSpecError):
            _ = test_suite.current_test_cache_dir

        with pytest.raises(spack.install_test.TestSuiteSpecError):
            _ = test_suite.current_test_data_dir

    spec = spack.spec.Spec('libelf').concretized()
    test_suite = spack.install_test.TestSuite([spec], 'test-cache')

    # Check no current specs yield failure
    ensure_current_cache_fail(test_suite)

    # Check no current base spec yields failure
    test_suite.current_base_spec = None
    test_suite.current_test_spec = spec
    ensure_current_cache_fail(test_suite)

    # Check no current test spec yields failure
    test_suite.current_base_spec = spec
    test_suite.current_test_spec = None
    ensure_current_cache_fail(test_suite)


def test_test_spec_run_once(mock_packages, install_mockery, mock_test_stage):
    spec = spack.spec.Spec('libelf').concretized()
    test_suite = spack.install_test.TestSuite([spec], 'test-dups')
    (test_suite.specs[0]).package.test_suite = test_suite

    with pytest.raises(spack.install_test.TestSuiteFailure):
        test_suite()


def test_test_spec_verbose(mock_packages, install_mockery, mock_test_stage):
    spec = spack.spec.Spec('simple-standalone-test').concretized()
    test_suite = spack.install_test.TestSuite([spec])

    test_suite(verbose=True)
    passed, msg = False, False
    with open(test_suite.log_file_for_spec(spec), 'r') as fd:
        for line in fd:
            if 'simple stand-alone test' in line:
                msg = True
            elif 'PASSED' in line:
                passed = True

    assert msg
    assert passed


def test_get_test_suite():
    assert not spack.install_test.get_test_suite('nothing')


def test_get_test_suite_no_name(mock_packages, mock_test_stage):
    with pytest.raises(spack.install_test.TestSuiteNameError) as exc_info:
        spack.install_test.get_test_suite('')

    assert 'name is required' in str(exc_info)


def test_get_test_suite_too_many(mock_packages, mock_test_stage):
    test_suites = []
    name = 'duplicate-alias'

    def add_suite(package):
        spec = spack.spec.Spec(package).concretized()
        suite = spack.install_test.TestSuite([spec], name)
        suite.ensure_stage()
        spack.install_test.write_test_suite_file(suite)
        test_suites.append(suite)

    add_suite('libdwarf')
    suite = spack.install_test.get_test_suite(name)
    assert suite.alias == name

    add_suite('libelf')
    with pytest.raises(spack.install_test.TestSuiteNameError) as exc_info:
        spack.install_test.get_test_suite(name)
    assert 'many suites named' in str(exc_info)
