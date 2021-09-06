# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hiop(CMakePackage, CudaPackage):
    """HiOp is an optimization solver for solving certain mathematical
    optimization problems expressed as nonlinear programming problems.
    HiOp is a lightweight HPC solver that leverages application's existing
    data parallelism to parallelize the optimization iterations by using
    specialized linear algebra kernels."""

    homepage = "https://github.com/LLNL/hiop"
    git = "https://github.com/LLNL/hiop.git"
    maintainers = ['ashermancinelli', 'CameronRutherford']

    # Most recent tagged snapshot is the preferred version when profiling.
    version('0.4.6', commit='b72d163d52c9225c3196ceb2baebdc7cf09a69de')
    version('0.4.5', commit='c353580456c4776c50811b97cf8ff802dc27b90c')
    version('0.4.4', commit='e858eefa6b914f5c87c3717bbce811931ea69386')
    version('0.4.3', commit='c0394af4d84ebb84b7d2b95283ad65ffd84e0d45')
    version('0.4.2', commit='3fcb788d223eec24c0241680070c4a9a5ec71ef3')
    version('0.4.1', commit='3f269560f76d5a89bcbd1d3c4f9f0e5acaa6fd64')
    version('0.4', commit='91d21085a1149eacdb27cd738d4a74a7e412fcff')
    version('0.3.99.3', commit='bed1dbef260e53a9d139ccfb77d2e83a98aab216')
    version('0.3.99.2', commit='9eb026768bc5e0a2c1293d0487cc39913001ae19')
    version('0.3.99.1', commit='220e32c0f318665d6d394ca3cd0735b9d26a65eb')
    version('0.3.99.0', commit='589b9c76781447108fa55788d5fa1b83ff71a3d1')
    version('0.3', commit='7e8adae9db757aed48e5c2bc448316307598258f')
    version('0.2', commit='c52a6f6b9baaaa2d7f233a749aa98f901349723f')
    version('0.1', commit='5f60e11b79d532115fb41694378b54c9c707aad9')

    # Development branches
    version('master', branch='master')
    version('develop', branch='develop')

    variant(
        'jsrun',
        default=False,
        description='Enable/Disable jsrun command for testing')
    variant(
        'shared',
        default=False,
        description='Enable/Disable shared libraries')
    variant('mpi', default=True, description='Enable/Disable MPI')
    variant('raja', default=False, description='Enable/Disable RAJA')
    variant('kron', default=False, description='Enable/Disable Kron reduction')
    variant(
        'sparse',
        default=False,
        description='Enable/Disable Sparse linear algebra')
    variant('deepchecking', default=False,
            description='Ultra safety checks - '
            'used for increased robustness and self-diagnostics')

    depends_on('lapack')
    depends_on('blas')
    depends_on('cmake@3.18:', type='build')

    depends_on('mpi', when='+mpi')

    depends_on('magma', when='+cuda')
    depends_on('magma@2.5.4:', when='@0.3.99.1:+cuda')
    depends_on('magma@2.6.1:', when='@0.4.6:+cuda')

    depends_on('raja', when='+raja')
    depends_on('umpire', when='+raja')

    depends_on('suite-sparse', when='+kron')

    depends_on('coinhsl', when='+sparse')
    depends_on('metis', when='+sparse')

    flag_handler = build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        lapack_blas_libs = (
            spec['lapack'].libs + spec['blas'].libs).joined(';')
        args.extend([
            '-DLAPACK_FOUND=TRUE',
            '-DLAPACK_LIBRARIES={0}'.format(lapack_blas_libs)
        ])

        args.append(self.define_from_variant('HIOP_BUILD_SHARED', 'shared'))
        args.append(self.define_from_variant('HIOP_USE_MPI', 'mpi'))
        args.append(self.define_from_variant('HIOP_DEEPCHECKS', 'deepchecking'))
        args.append(self.define_from_variant('HIOP_USE_GPU', 'cuda'))
        args.append(self.define_from_variant('HIOP_USE_CUDA', 'cuda'))
        args.append(self.define_from_variant('HIOP_USE_MAGMA', 'cuda'))
        args.append(self.define_from_variant('HIOP_USE_RAJA', 'raja'))
        args.append(self.define_from_variant('HIOP_USE_UMPIRE', 'raja'))
        args.append(self.define_from_variant('HIOP_WITH_KRON_REDUCTION', 'kron'))
        args.append(self.define_from_variant('HIOP_SPARSE', 'sparse'))
        args.append(self.define_from_variant('HIOP_USE_COINHSL', 'sparse'))
        args.append(self.define_from_variant('HIOP_TEST_WITH_BSUB', 'jsrun'))

        if '+mpi' in spec:
            args.append('-DMPI_HOME={0}'.format(spec['mpi'].prefix))
            args.append('-DMPI_C_COMPILER={0}'.format(spec['mpi'].mpicc))
            args.append('-DMPI_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx))
            args.append('-DMPI_Fortran_COMPILER={0}'.format(spec['mpi'].mpifc))

        # HIP flags are a part of the buildsystem, but full support is not
        # yet ready for public release
        args.append("-DHIOP_USE_HIP=OFF")

        if '+cuda' in spec:
            cuda_arch_list = spec.variants['cuda_arch'].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != 'none':
                args.append("-DHIOP_NVCC_ARCH=sm_{0}".format(cuda_arch))
                args.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch))
            if '+magma' in spec:
                args.append(
                    "-DHIOP_MAGMA_DIR={0}".format(spec['magma'].prefix))

        if '+kron' in spec:
            args.append(
                "-DHIOP_UMFPACK_DIR={0}".format(spec['suite-sparse'].prefix))

        # Unconditionally disable strumpack, even when +sparse. This may be
        # used in place of COINHSL for sparse interface, however this is not
        # fully supported in spack at the moment.
        args.append("-DHIOP_USE_STRUMPACK=OFF")

        if '+sparse' in spec:
            args.append(
                "-DHIOP_COINHSL_DIR={0}".format(spec['coinhsl'].prefix))

        return args
