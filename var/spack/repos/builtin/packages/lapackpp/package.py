# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lapackpp(CMakePackage):
    """LAPACK++: C++ API for the Basic Linear Algebra Subroutines (University
    of Tennessee)"""

    homepage = "https://bitbucket.org/icl/lapackpp"
    hg       = "https://bitbucket.org/icl/lapackpp"
    maintainers = ['teonnik', 'Sely85']

    version('develop', hg=hg, revision="7ffa486")

    variant('shared', default=True,
            description='Build a shared version of the library')

    depends_on('blaspp')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DBUILD_LAPACKPP_TESTS:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]
