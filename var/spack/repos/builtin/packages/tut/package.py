# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tut(WafPackage):
    """TUT is a small and portable unit test framework for C++."""

    homepage = "http://mrzechonek.github.io/tut-framework/"
    url      = "https://github.com/mrzechonek/tut-framework/tarball/2016-12-19"

    version('2016-12-19', '8b1967fa295ae1ce4d4431c2f811e521')

    patch('python3-octal.patch', when='@2016-12-19')

    def build_args(self):
        args = []

        if self.run_tests:
            # Run unit tests
            args.append('--test')

        return args
