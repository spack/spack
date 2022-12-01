# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TestFail(Package):
    """This package has a test method that fails in a subprocess."""

    homepage = "http://www.example.com/test-failure"
    url = "http://www.test-failure.test/test-failure-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def test_noop(self):
        """trigger test failure"""
        python = which("python")

        # Deliberately trigger a command failure
        python("-c", "noop", output=str.split, error=str.split)
