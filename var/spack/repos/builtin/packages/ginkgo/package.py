# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Ginkgo(CMakePackage, CudaPackage):
    """High-performance linear algebra library for manycore systems,
    with a focus on sparse solution of linear systems."""

    homepage = "https://ginkgo-project.github.io/"
    git      = "https://github.com/ginkgo-project/ginkgo.git"

    maintainers = ['tcojean', 'hartwiganzt']

    version('develop', branch='develop')
    version('master', branch='master')
    version('1.1.0', commit='b9bec8225442b3eb2a85a870efa112ab767a17fb')  # v1.1.0
    version('1.0.0', commit='45244641e0c2b19ba33aecd25153c0bddbcbe1a0')  # v1.0.0

    variant('shared', default=True, description='Build shared libraries')
    variant('full_optimizations', default=False, description='Compile with all optimizations')
    variant('openmp', default=sys.platform != 'darwin',  description='Build with OpenMP')
    variant('develtools', default=False, description='Compile with develtools enabled')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    depends_on('cmake@3.9:', type='build')
    depends_on('cuda@9:',    when='+cuda')

    conflicts('%gcc@:5.2.9')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DGINKGO_BUILD_CUDA=%s' % ('ON' if '+cuda' in spec else 'OFF'),
            '-DGINKGO_BUILD_OMP=%s' % ('ON' if '+openmp' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if '+shared' in spec else 'OFF'),
            '-DGINKGO_JACOBI_FULL_OPTIMIZATIONS=%s' % (
                'ON' if '+full_optimizations' in spec else 'OFF'),
            '-DGINKGO_DEVEL_TOOLS=%s' % (
                'ON' if '+develtools' in spec else 'OFF'),
            # As we are not exposing benchmarks, examples, tests nor doc
            # as part of the installation, disable building them altogether.
            '-DGINKGO_BUILD_BENCHMARKS=OFF',
            '-DGINKGO_BUILD_DOC=OFF',
            '-DGINKGO_BUILD_EXAMPLES=OFF',
            '-DGINKGO_BUILD_TESTS=OFF'
        ]
