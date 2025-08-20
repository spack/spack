# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.concretize
import spack.main
import spack.spec


@pytest.mark.not_on_windows("Logger test write fails on Windows")
@pytest.mark.usefixtures("mock_packages", "mock_fetch", "install_mockery")
def test_install_time_test_log_contains_check_and_installcheck():
    spec = spack.concretize.concretize_one(spack.spec.Spec("dummy-makefile-build-test-log@1.0"))

    # Install the package with --test=root to trigger check() and installcheck()
    install = spack.main.SpackCommand("install")
    install("--test=root", spec.name)

    # Get the expected path to the install-time test log
    log_path = os.path.join(spec.prefix, ".spack", "install-time-test-log.txt")
    assert os.path.exists(log_path), "Missing install-time-test-log.txt"

    with open(log_path, "r", encoding="utf-8") as f:
        contents = f.read()

    # Check that both dummy outputs are present
    assert "=== DUMMY MAKE TEST ===" in contents, "Missing 'make test' output"
    assert "=== DUMMY INSTALLCHECK ===" in contents, "Missing 'make installcheck' output"
