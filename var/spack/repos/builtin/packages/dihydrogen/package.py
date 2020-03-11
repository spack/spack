# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dihydrogen(CMakePackage, CudaPackage):
    """DiHydrogen is the second version of the Hydrogen fork of the
       well-known distributed linear algebra library,
       Elemental. DiHydrogen aims to be a basic distributed
       multilinear algebra interface with a particular emphasis on the
       needs of the distributed machine learning effort, LBANN."""

    homepage = "https://github.com/LLNL/DiHydrogen.git"
    git      = "https://github.com/LLNL/DiHydrogen.git"

    maintainers = ['bvanessen']

    version('master', branch='master')

    variant('al', default=True,
            description='Builds with Aluminum communication library')
    variant('developer', default=False,
            description='Enable extra warnings and force tests to be enabled.')
    variant('half', default=False,
            description='Enable FP16 support on the CPU.')
    variant('legacy', default=False,
            description='Enable the legacy DistConv code branch.')
    variant('nvshmem', default=False,
            description='Builds with support for NVSHMEM')
    variant('openmp', default=False,
            description='Enable CPU acceleration with OpenMP threads.')
    variant('rocm', default=False,
            description='Enable ROCm/HIP language features.')
    variant('shared', default=True,
            description='Enables the build of shared libraries')

    # Override the default set of CUDA architectures with the relevant
    # subset from lib/spack/spack/build_systems/cuda.py
    cuda_arch_values = [
        '60', '61', '62',
        '70', '72', '75',
    ]
    variant('cuda_arch',
            description='CUDA architecture',
            values=spack.variant.auto_or_any_combination_of(*cuda_arch_values))

    depends_on('mpi')
    depends_on('catch2', type='test')

    depends_on('aluminum', when='+al ~cuda')
    depends_on('aluminum +gpu +nccl +mpi_cuda', when='+al +cuda')

    depends_on('cuda', when=('+cuda' or '+legacy'))
    depends_on('cudnn', when=('+cuda' or '+legacy'))
    depends_on('cub', when=('+cuda' or '+legacy'))

    # Legacy builds require cuda
    conflicts('~cuda', when='+legacy')

    depends_on('half', when='+half')

    generator = 'Ninja'
    depends_on('ninja', type='build')
    depends_on('cmake@3.14.0:', type='build')

    illegal_cuda_arch_values = [
        '10', '11', '12', '13',
        '20', '21',
        '30', '32', '35', '37',
        '50', '52', '53',
    ]
    for value in illegal_cuda_arch_values:
        conflicts('cuda_arch=' + value)

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
            '-DBUILD_SHARED_LIBS:BOOL=%s'      % ('+shared' in spec),
            '-DH2_ENABLE_CUDA=%s' % ('+cuda' in spec),
            '-DH2_ENABLE_DISTCONV_LEGACY=%s' % ('+legacy' in spec),
            '-DH2_ENABLE_OPENMP=%s' % ('+openmp' in spec),
            '-DH2_ENABLE_FP16=%s' % ('+half' in spec),
            '-DH2_ENABLE_HIP_ROCM=%s' % ('+rocm' in spec),
            '-DH2_DEVELOPER_BUILD=%s' % ('+developer' in spec),
        ]

        if '+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            if len(cuda_arch) == 1 and cuda_arch[0] == 'auto':
                args.append('-DCMAKE_CUDA_FLAGS=-arch=sm_60')
            else:
                cuda_arch = [x for x in spec.variants['cuda_arch'].value
                             if x != 'auto']
                if cuda_arch:
                    args.append('-DCMAKE_CUDA_FLAGS={0}'.format(
                        ' '.join(self.cuda_flags(cuda_arch))
                    ))

        return args
