# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems import _checks as checks
from spack_repo.builtin_mock.build_systems import generic
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class TestBuildCallbacks(Package):
    """This package illustrates build callback test failure."""

    homepage = "http://www.example.com/test-build-callbacks"
    url = "http://www.test-failure.test/test-build-callbacks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")


class GenericBuilder(generic.GenericBuilder):
    phases = ["build", "install"]

    # Include undefined method (runtime failure)
    build_time_test_callbacks = ["undefined-build-test"]
    run_after("build")(checks.execute_build_time_tests)

    def build(self, pkg, spec, prefix):
        pass

    def install(self, pkg, spec, prefix):
        mkdirp(prefix.bin)
