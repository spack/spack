# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dihydrogen(CMakePackage):
    """DiHydrogen is the second version of the Hydrogen fork of the
       well-known distributed linear algebra library,
       Elemental. DiHydrogen aims to be a basic distributed
       multilinear algebra interface with a particular emphasis on the
       needs of the distributed machine learning effort, LBANN."""

    homepage = "https://github.com/LLNL/DiHydrogen.git"
    url      = "https://github.com/LLNL/DiHydrogen.git"
    git      = "https://github.com/LLNL/DiHydrogen.git"

    maintainers = ['bvanessen']

    version('master', branch='master')

    variant('al', default=True,
            description='Builds with Aluminum communication library')
    variant('cuda', default=False,
            description='Builds with support for GPUs via CUDA')
    variant('developer', default=False,
            description='Enable extra warnings and force tests to be enabled.')
    variant('half', default=False,
            description='Enable FP16 support on the CPU. Requires the Half library.')
    variant('legacy', default=False,
            description='Enable the legacy DistConv code branch.')
    variant('nvshmem', default=False,
            description='Builds with support for NVSHMEM')
    variant('openmp', default=False,
            description='Enable CPU acceleration with OpenMP threads.')
    variant('rocm', default=False,
            description='Search for and enable ROCm/HIP language features in DiHydrogen.')
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('test', default=False,
            description='Builds test suite')

    depends_on('mpi')
    depends_on('catch2', type='test')

    depends_on('aluminum', when='+al ~cuda')
    depends_on('aluminum +gpu +nccl +mpi_cuda', when='+al +cuda')

    depends_on('cuda', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('cub', when='+cuda')

    depends_on('half', when='+half')

    generator = 'Ninja'
    depends_on('ninja', type='build')
    depends_on('cmake@3.14.0:', type='build')

    @property
    def libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libH2Core', root=self.prefix, shared=shared, recursive=True
        )

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_INSTALL_MESSAGE:STRING=LAZY',
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DBUILD_SHARED_LIBS:BOOL=%s'      % ('+shared' in spec),
            '-DH2_ENABLE_CUDA=%s' % ('+cuda' in spec),
            '-DH2_ENABLE_DISTCONV_LEGACY=%s' % ('+legacy' in spec),
            '-DH2_ENABLE_OPENMP=%s' % ('+openmp' in spec),
            '-DH2_ENABLE_FP16=%s' % ('+half' in spec),
            '-DH2_ENABLE_HIP_ROCM=%s' % ('+rocm' in spec),
            '-DH2_DEVELOPER_BUILD=%s' % ('+developer' in spec),
            '-DCMAKE_CUDA_FLAGS=-arch=sm_60',
        ]

        return args
