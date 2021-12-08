# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TestWhens(Package):
    """This package has multiple test methods with when directives ."""

    homepage = "http://www.example.com/test-whens"
    url      = "http://www.test-whens.test/test-whens-1.0.tar.gz"

    version('1.1', '23456789abcdef0123456789abcdefg1')
    version('1.0', '123456789abcdef0123456789abcdef0')
    version('0.1', '0123456789abcdef0123456789abcdef')

    variant('var', default=False, description='Some variant')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    # Note that order matters (i.e., the first method that satisfies the
    # spec must (at least as of v0.17.0) appear first in the package).
    @when('@1.1 +var')
    def test(self):
        print("Tested 1.1 +var")

    @when('@1.0:')
    def test(self):
        print("Tested {0}".format(self.version))
