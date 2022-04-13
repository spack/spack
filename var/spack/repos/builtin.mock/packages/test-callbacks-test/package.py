# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import run_after


class TestCallbacksTest(Package):
    """This package illustrates callback test failure(s)."""

    homepage = "http://www.example.com/test-callback-test"
    url      = "http://www.test-failure.test/test-callback-test-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    # Include an undefined callback method
    install_time_test_callbacks = ['undefined-install-test', 'test']
    run_after('install')(Package._run_default_install_time_test_callbacks)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def test(self):
        raise Exception("Mock test failure")
