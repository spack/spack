# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GtkorvoAtl(CMakePackage):
    """Libatl provides a library for the creation and manipulation of
    lists of name/value pairs using an efficient binary representation.
    """

    homepage = "https://github.com/GTkorvo/atl"
    url      = "https://github.com/GTkorvo/atl/archive/v2.1.tar.gz"
    git      = "https://github.com/GTkorvo/atl.git"

    version('develop', branch='master')
    version('2.2', 'f0e3581e4b4c6943bf4b203685630564')
    version('2.1', 'b2324ff041bccba127330a0e1b241978')

    depends_on('gtkorvo-cercs-env')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('@2.2:'):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append('-DENABLE_TESTING=1')
        else:
            args.append('-DENABLE_TESTING=0')

        return args
