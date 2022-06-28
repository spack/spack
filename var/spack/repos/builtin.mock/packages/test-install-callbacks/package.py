# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.package_base import run_after


class TestInstallCallbacks(Package):
    """This package illustrates install callback test failure."""

    homepage = "http://www.example.com/test-install-callbacks"
    url      = "http://www.test-failure.test/test-install-callbacks-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    # Include an undefined callback method
    install_time_test_callbacks = ['undefined-install-test', 'test']
    run_after('install')(Package._run_default_install_time_test_callbacks)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def test(self):
        print('test: test-install-callbacks')
        print('PASSED')
