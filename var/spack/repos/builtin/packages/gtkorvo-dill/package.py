# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GtkorvoDill(CMakePackage):
    """DILL provides instruction-level code generation,
    register allocation and simple optimizations for generating
    executable code directly into memory regions for immediate use.
    """

    homepage = "https://github.com/GTkorvo/dill"
    url      = "https://github.com/GTkorvo/dill/archive/v2.1.tar.gz"
    git      = "https://github.com/GTkorvo/dill.git"

    version('develop', branch='master')
    version('2.4', '6836673b24f395eaae044b8bb976511d')
    version('2.1', '14c835e79b66c9acd2beee01d56e6200')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('@2.4:'):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append('-DENABLE_TESTING=1')
        else:
            args.append('-DENABLE_TESTING=0')

        return args
