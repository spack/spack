# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class HmatOss(CMakePackage):
    """A hierarchical matrix C/C++ library including a LU solver.
    """

    homepage = "https://github.com/jeromerobert/hmat-oss"
    url      = "https://github.com/jeromerobert/hmat-oss/archive/1.6.1.tar.gz"

    version('1.6.1', sha256='1517be8bde1c06bd8bc42d95926c72d787af95fc3d37439c911a7cea3243d2ca')
    version('1.5.0', sha256='21a64d1df1c9bb7221205020b95af8bff65668d0d2cfde5431d0e9fc7958d0a9')
    version('1.4.0', sha256='2fa08210e1ae5b40728c5bdc3a1001546b6271ea3fcbd39e53000bbe31c463bb')
    version('1.2.0', sha256='e52eefa6d34d338104c7058f11f724912d6a3626bce4101b5f798c3ab93f383c')

    variant('openmp', default=False, description='Enable OpenMP support')
    variant('jemalloc', default=False, description='Enable jemalloc support')

    depends_on('lapack')
    depends_on('blas')
    depends_on('jemalloc', when='+jemalloc')

    def cmake_args(self):
        args = [
            # Typo in option name, it should say ENABLE
            '-DHMAT_DISABLE_OPENMP=%s' % (
                'ON' if '+openmp' in self.spec else 'OFF'),
            '-DHMAT_JEMALLOC=%s' % (
                'ON' if '+jemalloc' in self.spec else 'OFF')
        ]

        return args
