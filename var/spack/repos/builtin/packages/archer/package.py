# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Archer(CMakePackage):
    """ARCHER, a data race detection tool for large OpenMP applications."""

    homepage = "https://github.com/PRUNERS/ARCHER"
    url      = "https://github.com/PRUNERS/archer/archive/v1.0.0.tar.gz"

    version('1.0.0', '790bfaf00b9f57490eb609ecabfe954a')

    depends_on('cmake@3.4.3:', type='build')
    depends_on('llvm')
    depends_on('ninja@1.5:', type='build')
    depends_on('llvm-openmp-ompt')

    generator = 'Ninja'

    def cmake_args(self):
        return [
            '-DCMAKE_C_COMPILER=clang',
            '-DCMAKE_CXX_COMPILER=clang++',
            '-DOMP_PREFIX:PATH=%s' % self.spec['llvm-openmp-ompt'].prefix,
        ]
