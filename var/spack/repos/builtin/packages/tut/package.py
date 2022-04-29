# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Tut(WafPackage):
    """TUT is a small and portable unit test framework for C++."""

    homepage = "https://mrzechonek.github.io/tut-framework/"
    url      = "https://github.com/mrzechonek/tut-framework/tarball/2016-12-19"

    version('2016-12-19', sha256='9fc0325d6db9709cc5213773bf4fd84f2a95154f18f7f8a553e1e52392e15691')

    patch('python3-octal.patch', when='@2016-12-19')

    # Python 3.7 support is currently broken
    # https://github.com/mrzechonek/tut-framework/issues/18
    depends_on('python@:3.6', type='build')

    # Tut is used for smoke build tests in CI, and started failing as
    # soon as gcc@11 was introduced in the environment
    conflicts('%gcc@11:')

    def build_args(self):
        args = []

        if self.run_tests:
            # Run unit tests
            args.append('--test')

        return args
