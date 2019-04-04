# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Ginkgo(CMakePackage, CudaPackage):
    """High-performance linear algebra library for manycore systems,
    with a focus on sparse solution of linear systems."""

    homepage = "https://github.com/ginkgo-project/ginkgo"
    url      = "https://github.com/ginkgo-project/ginkgo.git"
    git      = "https://github.com/ginkgo-project/ginkgo.git"

    version('develop', branch='develop')

    # Ginkgo has problems with circular dependencies and shared libs, see
    # https://github.com/ginkgo-project/ginkgo/issues/203
    # Thus keep default to False for now
    variant('shared', default=False, description='Build shared libraries')
    variant('openmp', default=sys.platform != 'darwin',  description='Build with OpenMP')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    depends_on('cmake@3.9:', type='build')
    depends_on('cuda@9:',    when='+cuda')

    # issues with ** expression, see
    # https://github.com/ginkgo-project/ginkgo/issues/270#issuecomment-473901621
    patch('static.patch')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DGINKGO_BUILD_CUDA=%s' % ('ON' if '+cuda' in spec else 'OFF'),
            '-DGINKGO_BUILD_OMP=%s' % ('ON' if '+openmp' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if '+shared' in spec else 'OFF'),
            '-DGINKGO_BUILD_BENCHMARKS=OFF'
        ]
