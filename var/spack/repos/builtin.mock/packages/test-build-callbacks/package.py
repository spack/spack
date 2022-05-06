# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import run_after


class TestBuildCallbacks(Package):
    """This package illustrates build callback test failure."""

    homepage = "http://www.example.com/test-build-callbacks"
    url      = "http://www.test-failure.test/test-build-callbacks-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    phases = ['build', 'install']
    # Include undefined method (runtime failure) and 'test' (audit failure)
    build_time_test_callbacks = ['undefined-build-test', 'test']
    run_after('build')(Package._run_default_build_time_test_callbacks)

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def test(self):
        print('test: running test-build-callbacks')
        print('PASSED')
