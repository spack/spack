# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import os
import sys

import pytest

import spack.install_test
import spack.spec

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="Tests fail on Windows")


def _true(*args, **kwargs):
    """Generic monkeypatch function that always returns True."""
    return True


def ensure_results(filename, expected):
    assert os.path.exists(filename)
    with open(filename, "r") as fd:
        lines = fd.readlines()
        have = False
        for line in lines:
            if expected in line:
                have = True
                break
        assert have


def test_test_log_pathname(mock_packages, config):
    """Ensure test log path is reasonable."""
    spec = spack.spec.Spec("libdwarf").concretized()

    test_name = "test_name"

    test_suite = spack.install_test.TestSuite([spec], test_name)
    logfile = test_suite.log_file_for_spec(spec)

    assert test_suite.stage in logfile
    assert test_suite.test_log_name(spec) in logfile


def test_test_ensure_stage(mock_test_stage, mock_packages):
    """Make sure test stage directory is properly set up."""
    spec = spack.spec.Spec("libdwarf").concretized()

    test_name = "test_name"

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.ensure_stage()

    assert os.path.isdir(test_suite.stage)
    assert mock_test_stage in test_suite.stage


def test_write_test_result(mock_packages, mock_test_stage):
    """Ensure test results written to a results file."""
    spec = spack.spec.Spec("libdwarf").concretized()
    result = "TEST"
    test_name = "write-test"

    test_suite = spack.install_test.TestSuite([spec], test_name)
    test_suite.ensure_stage()
    results_file = test_suite.results_file
    test_suite.write_test_result(spec, result)

    with open(results_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1

        msg = lines[0]
        assert result in msg
        assert spec.name in msg


def test_test_uninstalled(mock_packages, install_mockery, mock_test_stage):
    """Attempt to perform stand-alone test for uninstalled package."""
    spec = spack.spec.Spec("trivial-smoke-test").concretized()
    test_suite = spack.install_test.TestSuite([spec])

    test_suite()

    ensure_results(test_suite.results_file, "SKIPPED")
    ensure_results(test_suite.log_file_for_spec(spec), "Skipped not installed")


@pytest.mark.parametrize(
    "arguments,status,msg",
    [({}, "SKIPPED", "Skipped"), ({"externals": True}, "NO-TESTS", "No tests")],
)
def test_test_external(
    mock_packages, install_mockery, mock_test_stage, monkeypatch, arguments, status, msg
):
    name = "trivial-smoke-test"
    spec = spack.spec.Spec(name).concretized()
    spec.external_path = "/path/to/external/{0}".format(name)

    monkeypatch.setattr(spack.spec.Spec, "installed", _true)

    test_suite = spack.install_test.TestSuite([spec])
    test_suite(**arguments)

    ensure_results(test_suite.results_file, status)
    if arguments:
        ensure_results(test_suite.log_file_for_spec(spec), msg)


def test_test_stage_caches(mock_packages, install_mockery, mock_test_stage):
    def ensure_current_cache_fail(test_suite):
        with pytest.raises(spack.install_test.TestSuiteSpecError):
            _ = test_suite.current_test_cache_dir

        with pytest.raises(spack.install_test.TestSuiteSpecError):
            _ = test_suite.current_test_data_dir

    spec = spack.spec.Spec("libelf").concretized()
    test_suite = spack.install_test.TestSuite([spec], "test-cache")

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
    spec = spack.spec.Spec("libelf").concretized()
    test_suite = spack.install_test.TestSuite([spec], "test-dups")
    (test_suite.specs[0]).package.test_suite = test_suite

    with pytest.raises(spack.install_test.TestSuiteFailure):
        test_suite()


def test_test_spec_passes(mock_packages, install_mockery, mock_test_stage, monkeypatch):
    spec = spack.spec.Spec("simple-standalone-test").concretized()
    monkeypatch.setattr(spack.spec.Spec, "installed", _true)
    test_suite = spack.install_test.TestSuite([spec])
    test_suite()

    ensure_results(test_suite.results_file, "PASSED")
    ensure_results(test_suite.log_file_for_spec(spec), "simple stand-alone")


def test_get_test_suite():
    assert not spack.install_test.get_test_suite("nothing")


def test_get_test_suite_no_name(mock_packages, mock_test_stage):
    with pytest.raises(spack.install_test.TestSuiteNameError) as exc_info:
        spack.install_test.get_test_suite("")

    assert "name is required" in str(exc_info)


def test_get_test_suite_too_many(mock_packages, mock_test_stage):
    test_suites = []
    name = "duplicate-alias"

    def add_suite(package):
        spec = spack.spec.Spec(package).concretized()
        suite = spack.install_test.TestSuite([spec], name)
        suite.ensure_stage()
        spack.install_test.write_test_suite_file(suite)
        test_suites.append(suite)

    add_suite("libdwarf")
    suite = spack.install_test.get_test_suite(name)
    assert suite.alias == name

    add_suite("libelf")
    with pytest.raises(spack.install_test.TestSuiteNameError) as exc_info:
        spack.install_test.get_test_suite(name)
    assert "many suites named" in str(exc_info)


@pytest.mark.parametrize(
    "virtuals,names", [(False, False), (False, True), (True, False), (True, True)]
)
def test_test_functions(mock_packages, install_mockery, virtuals, names):
    spec = spack.spec.Spec("printing-package").concretized()
    expected = "printing-package.test" if names else "test"

    def check_results(fns):
        tests = fns if names else [f.__name__ for f in fns]
        assert len(tests) == 1, "expecting only one test function"
        assert tests[0] == expected

    fns = spack.install_test.test_functions(spec.package, add_virtuals=virtuals, names=names)
    check_results(fns)

    fns = spack.install_test.test_functions(
        spec.package.__class__, add_virtuals=virtuals, names=names
    )
    check_results(fns)


def test_test_package_class_unknown(mock_packages, ensure_debug, capsys):
    """Ensure expected result for existing mock virtual spec with no package."""
    vspec = spack.spec.Spec("something")
    cls = spack.install_test.package_class(vspec)
    out = capsys.readouterr()
    assert not cls, "Expected the package-less virtual spec to not have a package"
    assert "Cannot retrieve class from spec" in out[1]
    assert "not found" in out[1]


def test_test_functions_error_or_none(mock_packages):
    """Ensure expected results when test_functions called with incorrect values."""
    flag = spack.spec.CompilerFlag("cflags")
    with pytest.raises(ValueError):
        _ = spack.install_test.test_functions(flag)

    with pytest.raises(ValueError):
        _ = spack.install_test.test_functions(flag.__class__)


# TODO: This test should go away when compilers as dependencies is supported
def test_test_virtuals():
    # This is an unrealistic case but it is set up to retrieve all possible
    # virtual names in a single call.
    def satisfies(spec):
        return True

    # Ensure spec will pick up the llvm+clang virtual compiler package names.
    VirtualSpec = collections.namedtuple("VirtualSpec", ["name", "satisfies"])
    vspec = VirtualSpec("llvm", satisfies)

    # Ensure the package name is in the list that provides c, cxx, and fortran
    # to pick up the three associated compilers and that virtuals provided will
    # be deduped.
    MyPackage = collections.namedtuple("MyPackage", ["name", "spec", "virtuals_provided"])
    pkg = MyPackage("gcc", vspec, [vspec, vspec])

    # This check assumes the method will not provide a unique set of
    # compilers
    v_names = spack.install_test.virtuals(pkg)
    for name, number in [("c", 2), ("cxx", 2), ("fortran", 1), ("llvm", 1)]:
        assert v_names.count(name) == number, "Expected {0} of '{1}'".format(number, name)
