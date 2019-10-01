# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class F18(CMakePackage):
    """F18 is a front-end for Fortran intended to replace the existing front-end
    in the Flang compiler"""

    homepage = "https://github.com/flang-compiler/f18"

    git      = "https://github.com/flang-compiler/f18"

    version('develop', branch='master')

    depends_on('llvm@6.0.0+clang', when='@develop')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("spack-build/tools/f18/bin/f18", prefix.bin)
